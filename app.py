import re
import json
import html
import requests
import streamlit as st
import pandas as pd
from io import BytesIO
from openai import OpenAI

# For PDF creation
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from PIL import Image as PILImage
from markdown import markdown
from bs4 import BeautifulSoup

from prompts import dataset_context

st.set_page_config(page_title="Moshiach.ai")


###############################################################################
# GLOBAL SETTINGS
###############################################################################
VERBOSITY = 0  # 0 => Hide Agents #1, #2 outputs. Only show final summary (Agent #3) + images
               # 1 => Show everything (Agent #1 plan, Agent #2 code, etc.)

###############################################################################
# 0) SETUP & CONFIG
###############################################################################
API_KEY = st.secrets['API_KEY']
client = OpenAI(api_key=API_KEY)

###############################################################################
# 1) TABS UI
###############################################################################
tab1, tab2 = st.tabs(["AI Analyst", "Proposal Evaluator"])

###############################################################################
# 1A) APP INTRO (UNDER TAB #1)
###############################################################################
with tab1:
    st.title("Moshiach.ai [v0]")
    st.subheader("AI-Powered Interactive Data Analyst")
    with st.expander("How to Use", expanded=True):
        st.write(
            """
            1. **Enter your question** in the box below (for example, *"Which five factors best predict interest in The Alef?"*).
               - The more specific and clear your question, the better the results!
            2. **Click "Submit Query"**. The system will process your request and generate a response.
            3. **If the first response isn’t ideal**, simply ask a follow-up question using "Follow Up Question," or start over with "New Question."
               - Don’t worry if it’s not perfect on the first try—just click "Follow Up Question" and explain what missed the mark.
            4. **Download** your final summary and any generated plots as a PDF (see the button on the bottom right).
               - **Important**: The system does NOT store your responses or queries. If you want to keep the results, either download the PDF or copy the text you need into a document.
            
            *Under the hood, this tool uses an AI-optimized version of the original data and selects the best method (numeric or text analysis) to produce a concise final answer. Every query invokes three discrete AI agents that go to work providing the best answer possible.* 
            """
        )

###############################################################################
# 1B) TAB #2 - PROPOSAL EVALUATOR
###############################################################################
with tab2:
    st.write("TODO (Proposal Evaluator will be implemented here).")

###############################################################################
# 2) SETUP & FILE UPLOAD
###############################################################################
from cryptography.fernet import Fernet
from io import BytesIO

def load_and_decrypt_csv(encrypted_path: str) -> bytes:
    """
    Reads an .encrypted file from your repo and decrypts it using
    st.secrets["ENCRYPTION_KEY"]. Returns the plaintext CSV bytes.
    """
    # This key must match the one you used to encrypt the CSV locally (base64-encoded)
    encryption_key = st.secrets["ENCRYPTION_KEY"]  
    fernet = Fernet(encryption_key)

    with open(encrypted_path, "rb") as f:
        ciphertext = f.read()

    plaintext = fernet.decrypt(ciphertext)
    return plaintext

def setup_file_upload():
    """
    Replaces your existing setup_file_upload, but uses the encrypted CSV.
    """
    if "uploaded_file_id" not in st.session_state:
        st.write("Uploading dataset for AI...")
        try:
            # 1) Decrypt the CSV from 'super_cleaned_data.csv.encrypted'
            csv_plain_bytes = load_and_decrypt_csv("super_cleaned_data.csv.encrypted")

            # 2) Provide these bytes to client.files.create
            resp = client.files.create(
                file=BytesIO(csv_plain_bytes),
                purpose="assistants",
            )
            st.session_state["uploaded_file_id"] = resp.id
            st.success(f"Uploaded file ID: {resp.id}")
        except Exception as e:
            st.error(f"Error uploading CSV: {e}")
            st.stop()

    if "assistant_2_id" not in st.session_state:
        st.write("Initializing AI...")
        try:
            asst_2 = client.beta.assistants.create(
                name="Agent #2 - Code Interpreter",
                instructions=(
                    "You are Agent #2. You have a Code Interpreter tool that can analyze the CSV. "
                    "When the user provides Python code, run it on the CSV and return results."
                ),
                tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [st.session_state["uploaded_file_id"]]}},
                model="gpt-4o",
            )
            st.session_state["assistant_2_id"] = asst_2.id
            st.success(f"Agent #2 created. ID: {asst_2.id}")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating GPT-4 Code Interpreter: {e}")
            st.stop()

setup_file_upload()
###############################################################################
# 3) SESSION STATE
###############################################################################
if "agent1_messages" not in st.session_state:
    st.session_state["agent1_messages"] = []
if "agent2_combined_outputs" not in st.session_state:
    st.session_state["agent2_combined_outputs"] = ""
if "user_query_for_agent3" not in st.session_state:
    st.session_state["user_query_for_agent3"] = ""
if "next_prompt_type" not in st.session_state:
    st.session_state["next_prompt_type"] = "Ask any question about this dataset..."
if "agent2_thread_id" not in st.session_state:
    st.session_state["agent2_thread_id"] = None
if "agent2_image_file_ids" not in st.session_state:
    st.session_state["agent2_image_file_ids"] = []

# Store final summary & images for PDF
if "final_summary_markdown" not in st.session_state:
    st.session_state["final_summary_markdown"] = ""
if "cached_images" not in st.session_state:
    st.session_state["cached_images"] = []
if "user_query_for_pdf" not in st.session_state:
    st.session_state["user_query_for_pdf"] = ""

###############################################################################
# 4) IMAGE FETCH & DISPLAY
###############################################################################
def fallback_download_file(file_id: str) -> bytes:
    url = f"https://api.openai.com/v1/files/{file_id}/content"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.content

def fetch_image_bytes(file_id: str) -> bytes:
    """
    Attempt to read from OpenAI's library approach, else do direct GET fallback.
    """
    try:
        lib_obj = client.files.content(file_id)
        if hasattr(lib_obj, "read"):
            return lib_obj.read()
        elif isinstance(lib_obj, bytes):
            return lib_obj
    except Exception:
        pass
    try:
        return fallback_download_file(file_id)
    except Exception:
        return b""

def display_images_after_agent3():
    """
    For each file_id in agent2_image_file_ids, fetch the bytes, display in app,
    and store in cached_images for PDF. Then clear them from state.
    """
    st.session_state["cached_images"].clear()
    if not st.session_state["agent2_image_file_ids"]:
        return

    st.subheader("Plots / Images")
    for idx, fid in enumerate(st.session_state["agent2_image_file_ids"]):
        b_ = fetch_image_bytes(fid)
        if b_ and len(b_) > 0:
            st.image(b_, use_column_width=True)
            fn = f"plot_{idx+1}.png"
            st.session_state["cached_images"].append((fn, b_))
        else:
            st.error(f"Could not retrieve bytes for file_id={fid}")
    st.session_state["agent2_image_file_ids"].clear()

###############################################################################
# 5) AGENT #1
###############################################################################
def run_agent_1(user_query: str) -> str:
    """
    Returns JSON:
      {"type":"quantitative","code":"..."}
    or
      {"type":"qualitative","column":"...","prompt":"..."}
    """
    with st.spinner("Agent #1 is generating plan..."):
        try:
            llm_snippet = (
                "from openai import OpenAI\n"
                f"client = OpenAI(api_key='{API_KEY}')\n\n"
                "completion = client.chat.completions.create(\n"
                '  model="o3-mini-2025-01-31",\n'
                "  messages=[\n"
                '    {"role": "developer", "content": "You are a helpful assistant."},\n'
                '    {"role": "user", "content": "..."}\n'
                "  ]\n"
                ")\n\n"
                "print(completion.choices[0].message.content)\n"
            )

            instructions_for_agent1 = (
                "You are Agent #1. The dataset is 'super_cleaned_data.csv' with this schema:\n\n"
                f"{dataset_context}\n\n"
                "Decide if the question is numeric/quantitative vs. text/qualitative. "
                "If numeric => produce JSON:\n"
                '{"type":"quantitative","code":"(python for Agent2)"}\n\n'
                "If text => produce JSON:\n"
                '{"type":"qualitative","column":"somecol","prompt":"(instructions for the LLM). Please include direct quotes where possible."}\n\n'
                "If you do LLM calls, use the exact snippet:\n"
                f"{llm_snippet}\n"
                "Keep your plan minimal. Only do text-based approach if the user specifically wants quotes/text insights."
            )

            c = client.chat.completions.create(
                model="o3-mini-2025-01-31",
                reasoning_effort="high",
                messages=[
                    {"role": "developer", "content": instructions_for_agent1},
                    {"role": "user", "content": user_query},
                ],
            )
            return c.choices[0].message.content
        except Exception as e:
            return f"Error calling Agent #1: {e}"

###############################################################################
# 6) AGENT #2 (quantitative code)
###############################################################################
def run_agent_2(plan_code: str) -> str:
    with st.spinner("Agent #2 is running code..."):
        out_ = ""
        try:
            if st.session_state["agent2_thread_id"] is None:
                thr = client.beta.threads.create()
                st.session_state["agent2_thread_id"] = thr.id

            thread_id = st.session_state["agent2_thread_id"]
            asst_2id = st.session_state["assistant_2_id"]

            content_ = (
                "Here is the Python code from Agent #1. "
                "Please run it and provide all outputs (text, plots, data). "
                "Code:\n\n" + plan_code
            )

            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content_
            )

            run_ = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=asst_2id,
                instructions=(
                    "You are Agent #2 (GPT-4o Code Interpreter). Execute the code on 'super_cleaned_data.csv' and return all results."
                ),
            )

            msgs = client.beta.threads.messages.list(thread_id=thread_id)
            for m in msgs.data:
                if m.role == "assistant":
                    cval = m.content
                    if isinstance(cval, list):
                        for block in cval:
                            if isinstance(block, dict):
                                btype = block.get("type")
                                if btype == "text":
                                    txt_ = block["text"].get("value", "")
                                    out_ += txt_ + "\n\n"
                                elif btype in ["image_file", "ImageFileContentBlock"]:
                                    im = block.get("image_file", {})
                                    fid = im.get("file_id", "")
                                    out_ += f"[ImageFileContentBlock with file_id={fid}]\n"
                                    st.session_state["agent2_image_file_ids"].append(fid)
                                else:
                                    out_ += str(block) + "\n\n"
                            else:
                                block_str = str(block)
                                if "type='image_file'" in block_str:
                                    match = re.search(r"file_id='(file-[^']+)'", block_str)
                                    if match:
                                        out_ += f"[ImageFileContentBlock with file_id={match.group(1)}]\n"
                                        st.session_state["agent2_image_file_ids"].append(match.group(1))
                                else:
                                    out_ += block_str + "\n\n"
                    else:
                        out_ += str(cval) + "\n\n"
            return out_.strip()
        except Exception as ex:
            return f"Error calling Agent #2: {ex}"

###############################################################################
# 7) LOCAL LLM FOR QUALITATIVE
###############################################################################
def run_local_llm_on_text(column_name: str, prompt: str) -> str:
    with st.spinner("Agent #2 (Local LLM) analyzing text..."):
        try:
            df = pd.read_csv("super_cleaned_data.csv")
            if column_name not in df.columns:
                return f"Error: The column '{column_name}' is not found in the dataset."

            text_data = df[column_name].dropna().astype(str).tolist()
            joined_text = "\n".join(text_data)

            local_prompt = (
                prompt
                + "\n\n=== SAMPLE TEXT DATA ===\n"
                + joined_text
            )

            completion = client.chat.completions.create(
                model="o3-mini-2025-01-31",
                messages=[
                    {"role":"developer","content":"You are a helpful assistant that includes direct quotes if possible."},
                    {"role":"user","content":local_prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error during local LLM call: {e}"

###############################################################################
# 8) AGENT #3 QUANT + QUAL
###############################################################################
def run_agent_3_quant(user_q: str, plan_text: str, analysis_out: str) -> str:
    with st.spinner("Agent #3 is summarizing (quantitative)..."):
        try:
            final_msg = (
                f"You are Agent #3. The user asked:\n'{user_q}'\n\n"
                "Agent #1's plan/code:\n"
                f"{plan_text}\n\n"
                "Agent #2's code execution outputs:\n"
                f"{analysis_out}\n\n"
                "Please produce a concise final answer in **Markdown** with minimal jargon. "
                "Start with a direct numeric/statistical answer, then a short explanation. "
                "Do **not** embed any images or plots in your text. NEVER RETURN OR SHOW ANY CODE "
                "Do not mention 'agents' or the underlying process, and never suggest that the dataset needs further refinement/cleaning."
            )

            c = client.chat.completions.create(
                model="o3-mini-2025-01-31",
                reasoning_effort="high",
                messages=[
                    {
                        "role": "developer",
                        "content": "You are Agent #3. Summarize a quantitative analysis in plain Markdown with no mention of images."
                    },
                    {"role": "user", "content": final_msg}
                ]
            )
            return c.choices[0].message.content
        except Exception as e:
            return f"Error calling Agent #3 (quant): {e}"

def run_agent_3_qual(user_q: str, plan_text: str, analysis_out: str) -> str:
    with st.spinner("Agent #3 is summarizing (qualitative)..."):
        try:
            final_msg = (
                f"You are Agent #3. The user asked:\n'{user_q}'\n\n"
                "Agent #1's plan (qualitative text analysis):\n"
                f"{plan_text}\n\n"
                "Local LLM analysis outputs:\n"
                f"{analysis_out}\n\n"
                "Please produce a final answer in **Markdown** that emphasizes the rich text insights, "
                "including direct quotes if they appear in the analysis. Begin with a direct conclusion, then highlight any themes or sentiments. "
                "Do not mention 'agents' or the underlying process, just present the text-based findings in a structured, user-friendly manner."
            )

            c = client.chat.completions.create(
                model="o3-mini-2025-01-31",
                reasoning_effort="high",
                messages=[
                    {
                        "role": "developer",
                        "content": "You are Agent #3, summarizing a qualitative text analysis in plain Markdown with direct quotes."
                    },
                    {"role": "user", "content": final_msg}
                ]
            )
            return c.choices[0].message.content
        except Exception as e:
            return f"Error calling Agent #3 (qual): {e}"

###############################################################################
# 9) PDF GENERATION
###############################################################################
def generate_pdf(query: str, summary_markdown: str, images: list):
    """
    Convert user query + final summary (Markdown) + images into a PDF.
    We'll parse headings (#, ##, ###) using markdown->BeautifulSoup, then
    produce appropriate headings in the PDF. We'll do minimal coverage of tables/lists.
    """

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()

    styleH1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=10,
    )
    styleH2 = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=8,
    )
    styleH3 = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=6,
    )
    styleNormal = ParagraphStyle(
        'NormalCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=6,
    )

    styleList = ParagraphStyle(
        'List',
        parent=styleNormal,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=5,
    )

    story = []

    # 1) user query
    story.append(Paragraph(f"<b>User Query:</b> {html.escape(query)}", styleNormal))
    story.append(Spacer(1, 12))

    # 2) parse summary
    md_as_html = markdown(summary_markdown)
    soup = BeautifulSoup(md_as_html, 'html.parser')

    def handle_elem(elem):
        if elem.name == 'h1':
            text = elem.get_text()
            story.append(Paragraph(text, styleH1))
            story.append(Spacer(1, 6))
        elif elem.name == 'h2':
            text = elem.get_text()
            story.append(Paragraph(text, styleH2))
            story.append(Spacer(1, 6))
        elif elem.name == 'h3':
            text = elem.get_text()
            story.append(Paragraph(text, styleH3))
            story.append(Spacer(1, 6))
        elif elem.name in ['p']:
            story.append(Paragraph(str(elem), styleNormal))
            story.append(Spacer(1, 6))
        elif elem.name in ['ul', 'ol']:
            for li in elem.find_all('li', recursive=False):
                bullet_item = "• " + li.get_text()
                story.append(Paragraph(bullet_item, styleList))
        elif elem.name == 'table':
            # minimal approach
            table_data = []
            rows = elem.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                row_data = [c.get_text(strip=True) for c in cols]
                if row_data:
                    table_data.append(row_data)
            if table_data:
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ]))
                story.append(t)
                story.append(Spacer(1, 12))
        elif elem.name is None and isinstance(elem, str):
            text = elem.strip()
            if text:
                story.append(Paragraph(text, styleNormal))
                story.append(Spacer(1, 6))
        else:
            # fallback
            text = elem.get_text(strip=True)
            if text:
                story.append(Paragraph(text, styleNormal))
                story.append(Spacer(1, 6))

    for child in soup.children:
        if child.name:
            handle_elem(child)
        elif isinstance(child, str) and child.strip():
            story.append(Paragraph(child.strip(), styleNormal))
            story.append(Spacer(1, 6))

    # 3) images
    for idx, (fname, b_) in enumerate(images):
        story.append(Paragraph(f"Plot/Image {idx+1}:", styleNormal))
        story.append(Spacer(1, 6))
        try:
            pil_img = PILImage.open(BytesIO(b_))
            w, h = pil_img.size
            ratio = h / float(w) if w != 0 else 1.0
            max_w = 500.0
            t_h = ratio * max_w
            rlimg = RLImage(BytesIO(b_), width=max_w, height=t_h)
            story.append(rlimg)
        except Exception as e:
            story.append(Paragraph(f"Error embedding image: {e}", styleNormal))
        story.append(Spacer(1, 12))

    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

###############################################################################
# 10) MAIN PIPELINE
###############################################################################
def process_entire_pipeline(user_query: str):
    """
    If VERBOSITY=0, we hide Agent #1 plan and Agent #2 output expansions,
    otherwise we show them.
    """
    st.session_state["agent2_image_file_ids"].clear()

    # 1) AGENT #1
    agent1_plan = run_agent_1(user_query)

    if VERBOSITY > 0:
        with st.expander("Agent #1 Plan & Code", expanded=False):
            st.text(agent1_plan)

    # parse plan
    plan_type = "quantitative"
    analysis_output = ""
    try:
        parsed_plan = json.loads(agent1_plan)
        plan_type = parsed_plan.get("type","quantitative")
    except:
        parsed_plan = {}

    # 2) If quant => code with Agent #2, else => local snippet
    if plan_type == "quantitative":
        code_ = parsed_plan.get("code","")
        analysis_output = run_agent_2(code_)
        if VERBOSITY > 0:
            with st.expander("Agent #2 Output", expanded=False):
                st.text(analysis_output)
        agent3_out = run_agent_3_quant(user_query, agent1_plan, analysis_output)
    else:
        col_ = parsed_plan.get("column","")
        prompt_ = parsed_plan.get("prompt","")
        analysis_output = run_local_llm_on_text(col_, prompt_)
        if VERBOSITY > 0:
            with st.expander("Local LLM (Qualitative) Output", expanded=False):
                st.text(analysis_output)
        agent3_out = run_agent_3_qual(user_query, agent1_plan, analysis_output)

    # 3) Final summary displayed full-width
    st.divider()
    st.markdown("## Final Response")
    st.markdown(agent3_out)

    # 4) Possibly show images
    display_images_after_agent3()

    # 5) Cache final summary + user query for PDF
    st.session_state["final_summary_markdown"] = agent3_out
    st.session_state["user_query_for_pdf"] = user_query

    st.success("All steps completed.")

###############################################################################
# 11) RESET & FOLLOW-UP
###############################################################################
def reset_everything():
    st.session_state["agent1_messages"] = []
    st.session_state["agent2_combined_outputs"] = ""
    st.session_state["agent2_image_file_ids"].clear()
    st.session_state["final_summary_markdown"] = ""
    st.session_state["cached_images"] = []
    st.session_state["agent2_thread_id"] = None
    st.session_state["user_query_for_pdf"] = ""
    st.rerun()

###############################################################################
# 12) DOWNLOAD PDF
###############################################################################
def download_pdf():
    """Generate a PDF with the user's query, final summary, and images."""
    if not st.session_state.get("final_summary_markdown"):
        st.warning("No final summary to download yet.")
        return

    user_query = st.session_state.get("user_query_for_pdf","(no query saved)")
    summary_markdown = st.session_state["final_summary_markdown"]
    images = st.session_state["cached_images"]

    pdf_data = generate_pdf(user_query, summary_markdown, images)
    st.download_button(
        label="Download Results as PDF",
        data=pdf_data,
        file_name="results.pdf",
        mime="application/pdf",
    )

###############################################################################
# MAIN UI (TAB #1)
###############################################################################
with tab1:
    st.divider()
    prompt_placeholder = st.session_state["next_prompt_type"]
    user_input = st.text_area("Enter your question:", placeholder=prompt_placeholder)

    # Single row for submit
    if st.button("Submit Query"):
        if user_input.strip():
            process_entire_pipeline(user_input.strip())
            st.session_state["next_prompt_type"] = "Ask a follow-up question..."
        else:
            st.warning("Please enter a non-empty question.")

    st.divider()
    # Follow-up / New Q / Download PDF
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("Follow Up Question"):
            st.session_state["next_prompt_type"] = "Ask a follow-up question..."
            st.info("Enter your follow-up above and click 'Submit Query'.")

    with c2:
        if st.button("New Question"):
            reset_everything()
            st.info("Reset complete. Type a brand new question above.")

    with c3:
        download_pdf()
