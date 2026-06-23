import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Portable relative paths
pptx_path = "Smart Verse template _20260622_160530_0000.pptx"
output_path = "Smart_Verse_Lip2Speech_Presentation.pptx"

system_arch_path = os.path.join("static", "system_architecture.png")
perf_dashboard_path = os.path.join("static", "performance_dashboard.png")

if not os.path.exists(pptx_path):
    print(f"Error: PowerPoint template file not found at: {pptx_path}")
    import sys
    sys.exit(1)

prs = Presentation(pptx_path)
print(f"Loaded presentation template: {pptx_path}")

# Helper function to clear extra runs and set text in paragraph
def set_paragraph_text(p, text):
    if not p.runs:
        p.add_run().text = text
    else:
        p.runs[0].text = text
        for run in p.runs[1:]:
            run.text = ""

# Slide-by-slide modification
for idx, slide in enumerate(prs.slides, 1):
    print(f"Processing Slide {idx}...")
    
    # Slide 1: Title Slide
    if idx == 1:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Title of the Project" in text:
                    shape.text_frame.text = "Lip2Speech: Spatio-Temporal Lip Reading and Speech Synthesis for Assistive Communication"
                    # Apply styling to first paragraph
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(36)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Prepared by" in text:
                    shape.text_frame.text = "Prepared by:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(14)
                    p.font.name = "Outfit"
                elif "Team Name" in text:
                    shape.text_frame.text = "Smart Verse Team"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(20)
                    p.font.bold = True
                    p.font.name = "Outfit"

    # Slide 2: Team Members
    elif idx == 2:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "First Member Name" in text:
                    shape.text_frame.text = "Alekhya K"
                elif "Second Member Name" in text:
                    shape.text_frame.text = "[Insert Member 2]"
                elif "Third Member Name" in text:
                    shape.text_frame.text = "[Insert Member 3]"
                elif "Affiliation" in text:
                    shape.text_frame.text = "Department of Computer Science / Healthcare Informatics"
                elif "Email-ID" in text:
                    shape.text_frame.text = "contact@smartverse.ai"

    # Slide 3: Introduction
    elif idx == 3:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Our project aims to analyze" in text or "Our project aims to reconstruct" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p = tf.paragraphs[0]
                    p.text = "Our project reconstructs spoken audio from silent lip movements as a direct assistive voice for speech-impaired individuals. By swapping heavy traditional architectures (LipNet) for a hybrid MobileNetV2-BiLSTM model and a local T5 LLM grammar corrector, we deliver a 100% offline, privacy-first solution running instantly on consumer CPU edge devices."
                    p.font.size = Pt(16)
                    p.font.name = "Inter"
                    p.space_after = Pt(12)

    # Slide 4: Problem Statement
    elif idx == 4:
        # Clear any programmatically added textboxes from previous run to avoid duplicates
        shapes_to_remove = []
        for shape in slide.shapes:
            if shape.has_text_frame and shape.name.startswith("TextBox") and "Problem Statement" not in shape.text_frame.text:
                shapes_to_remove.append(shape)
        for shape in shapes_to_remove:
            try:
                slide.shapes._spTree.remove(shape._element)
            except:
                pass
                
        # 3-Column Problem Statement Layout
        cols_data = [
            {
                "title": "1. Social Barrier",
                "subtitle": "Daily Isolation",
                "desc": "Manual typing is too slow, disrupting conversational flow and causing social isolation.",
                "impact": "Impact: Speech-impaired individuals face high communication barriers."
            },
            {
                "title": "2. Environmental Barrier",
                "subtitle": "Acoustic Failures",
                "desc": "Voice recognition fails in loud environments (factories) or silent zones (hospitals).",
                "impact": "Impact: Traditional voice tools become unusable when needed most."
            },
            {
                "title": "3. Technical Barrier",
                "subtitle": "The Hardware Wall",
                "desc": "Heavy 3D CNN architectures require expensive cloud GPUs, leaking user data privacy.",
                "impact": "Impact: Prevents fast, offline, and secure execution on local edge devices."
            }
        ]
        
        col_width = Inches(5.0)
        col_gap = Inches(0.8)
        left_margin = Inches(1.0)
        top_pos = Inches(2.5)
        height = Inches(5.5)
        
        for c_idx, data in enumerate(cols_data):
            col_left = left_margin + c_idx * (col_width + col_gap)
            txBox = slide.shapes.add_textbox(col_left, top_pos, col_width, height)
            tf = txBox.text_frame
            tf.word_wrap = True
            
            # Title
            p0 = tf.paragraphs[0]
            p0.text = data["title"]
            p0.font.size = Pt(20)
            p0.font.bold = True
            p0.font.name = "Outfit"
            p0.space_after = Pt(4)
            
            # Subtitle
            p1 = tf.add_paragraph()
            p1.text = data["subtitle"]
            p1.font.size = Pt(16)
            p1.font.bold = True
            p1.font.name = "Outfit"
            p1.font.color.rgb = RGBColor(0, 102, 204) # Deep blue
            p1.space_after = Pt(12)
            
            # Description
            p2 = tf.add_paragraph()
            p2.text = "• " + data["desc"]
            p2.font.size = Pt(14)
            p2.font.name = "Inter"
            p2.space_after = Pt(12)
            
            # Impact
            p3 = tf.add_paragraph()
            p3.text = "• " + data["impact"]
            p3.font.size = Pt(14)
            p3.font.italic = True
            p3.font.name = "Inter"
            p3.font.color.rgb = RGBColor(128, 128, 128) # Grey

    # Slide 5: Motivation
    elif idx == 5:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Motivation is a key element" in text or "Restoring Independence" in text or "Autonomy" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    
                    bullets = [
                        "Autonomy: Restoring natural, visual-to-speech communication for speech-impaired individuals.",
                        "Privacy: 100% offline local execution, guaranteeing complete user data security.",
                        "Edge Run: Swapping compile-heavy C++ libraries (dlib) for fast, standard OpenCV cascades.",
                        "Low Latency: Instant speech reconstruction and synthesis in under 2.0s on standard edge CPUs."
                    ]
                    for i, bullet in enumerate(bullets):
                        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                        p.text = "• " + bullet
                        p.level = 0  # Fix paragraph indentation alignment
                        p.space_after = Pt(12)
                        p.font.size = Pt(16)
                        p.font.name = "Inter"

    # Slide 6: Domain
    elif idx == 6:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "In software engineering, a domain" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    
                    bullets = [
                        "Primary Domain: Healthcare Informatics & Assistive Communication Technology.",
                        "Computer Vision (Spatial Modeling): Frame-by-frame mouth extraction and spatial representation modeling using a pre-trained MobileNetV2 architecture.",
                        "Sequence Modeling (Temporal Processing): Modeling sequential video context over time using a 2-layer Bidirectional Long Short-Term Memory (BiLSTM) network.",
                        "Natural Language Processing (Text Refinement): Applying a sequence-to-sequence local T5 Transformer model to correct raw phoneme/word predictions.",
                        "Speech Synthesis (Acoustic Output): Generates high-fidelity spoken voice audio from refined text using pyttsx3 and gTTS fallbacks."
                    ]
                    for i, bullet in enumerate(bullets):
                        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                        p.text = "• " + bullet
                        p.level = 0  # Fix paragraph indentation alignment
                        p.space_after = Pt(12)
                        p.font.size = Pt(16)
                        p.font.name = "Inter"

    # Slide 7: Existing Solutions
    elif idx == 7:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Analysis Phase" in text or "LipNet" in text:
                    shape.text_frame.text = "1. LipNet (CTC)"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Analyze sales performance" in text or "character-level CTC" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• Model: LipNet (Character-level CTC)\n• Difficulty: High Word Error Rate on short words.\n• Compiler Wall: Requires C++ dlib/CMake bindings, causing edge setup failure."
                    p0.font.size = Pt(11)
                    p0.font.name = "Inter"
                    
                elif "Strategy Development" in text or "Transformers" in text:
                    shape.text_frame.text = "2. AV Transformers"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Create new strategies using" in text or "AV-HubERT" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• Models: AV-HubERT, Lip2Wav\n• Difficulty: Gigantic model parameter size & storage footprint.\n• GPU Wall: Requires desktop GPUs; completely freezes standard edge CPUs."
                    p0.font.size = Pt(11)
                    p0.font.name = "Inter"
                    
                elif "Implementation Plan" in text or "Cloud" in text:
                    shape.text_frame.text = "3. Cloud APIs"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Create a timeline with" in text or "Proprietary" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• Models: Proprietary cloud speech APIs\n• Difficulty: Requires continuous, high-bandwidth web connection.\n• Privacy Wall: Sends private video/audio files to cloud, risking data leaks."
                    p0.font.size = Pt(11)
                    p0.font.name = "Inter"

    # Slide 8: Methodology & System Architecture
    elif idx == 8:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Brainstorming Sessions:" in text:
                    shape.text_frame.text = "Spatio-Temporal Pipeline:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Collaborate to generate" in text or "Video Input" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "[Silent Video Input (25 FPS)]\n  ➔ OpenCV Haar Cascade Face Detection\n  ➔ Bounding Box Lower-Half Mouth Crop\n  ➔ Spatial Feature Extractor (MobileNetV2)\n  ➔ Temporal Sequence Modeler (BiLSTM)"
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"
                    
                elif "Testing and Refinement:" in text or "Correction & TTS:" in text:
                    shape.text_frame.text = "LLM Post-Correction & TTS Flow:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Pilot the proposed" in text or "Token Sequence" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "[Raw Word Token Sequence]\n  ➔ Argmax Vocabulary Greedy Decoding\n  ➔ Post-Inference Spelling & Grammar LLM (T5-Base)\n  ➔ Sentence Synthesis Refinement\n  ➔ Offline TTS Voice Feedback (pyttsx3/gTTS)"
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"
                    
        # Add system architecture diagram on the right side
        if os.path.exists(system_arch_path):
            slide.shapes.add_picture(system_arch_path, Inches(13.0), Inches(2.2), width=Inches(5.8), height=Inches(6.5))
            print("  Inserted system_architecture.png successfully.")

    # Slide 9: Data Analysis & Ablation Study
    elif idx == 9:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Over the past year" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "We benchmarked our model on the GRID Corpus (33,000 video-transcript pairs) to find the optimal configuration for edge-deployment. Shortening temporal frame context decreases compute time but increases loss drastically, proving a 25-frame context is necessary."
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"
                elif "Product 1" in text:
                    shape.text_frame.text = "Baseline (Frozen CNN + 25f)\nCompute Time: 13.9s | Training Loss: 1.72\nBest speed/accuracy balance."
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(12)
                    p.font.name = "Inter"
                elif "Product 2" in text:
                    shape.text_frame.text = "Ablation A (Unfrozen CNN + 25f)\nCompute Time: 15.1s | Training Loss: 1.69\nMarginally better loss but too heavy for CPU."
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(12)
                    p.font.name = "Inter"
                elif "Product 3" in text:
                    shape.text_frame.text = "Ablation B (Starved Context - 10f)\nCompute Time: 5.7s | Training Loss: 2.85\nFastest compute, but suffers high loss."
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(12)
                    p.font.name = "Inter"
                    
        # Add performance dashboard diagram on the left side
        if os.path.exists(perf_dashboard_path):
            slide.shapes.add_picture(perf_dashboard_path, Inches(0.5), Inches(2.2), width=Inches(11.5), height=Inches(8.0))
            print("  Inserted performance_dashboard.png successfully.")

    # Slide 10: Result & Metrics
    elif idx == 10:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Increased Sales Figures:" in text:
                    shape.text_frame.text = "High-Accuracy Speech Reconstruction:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Target a 25% increase" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• The T5 LLM grammar corrector resolves spelling and syntax errors from raw sequence-to-sequence decodings.\n• Collapses repetitive characters (e.g. converting 'set set white' into 'set white') for natural voice speech."
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"
                    
                elif "Enhanced Market Reach:" in text:
                    shape.text_frame.text = "Real-Time Edge Latency:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Expand market reach" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• Core model prediction and post-processing takes under 2.0 seconds on standard consumer laptop CPUs.\n• Zero latency variance because it runs entirely locally offline without network requests."
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"
                    
                elif "Improved Customer Engagement:" in text:
                    shape.text_frame.text = "Cross-Platform Deployment:"
                    p = shape.text_frame.paragraphs[0]
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.name = "Outfit"
                elif "Foster stronger relationships" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    p0 = tf.paragraphs[0]
                    p0.text = "• Packaged within a lightweight, CPU-optimized Docker container using a Flask server architecture.\n• Deployed on local host (port 5000) and Hugging Face Spaces (port 7860)."
                    p0.font.size = Pt(13)
                    p0.font.name = "Inter"

    # Slide 11: Future Scope
    elif idx == 11:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "A project scope is a detailed outline" in text or "Continuous Vocabulary Expansion" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    
                    bullets = [
                        "Continuous Real-Time System: Develop an automated streaming system that continuously captures live webcam frames, runs sliding-window lip-detection, and synthesizes speech on-the-fly.",
                        "AV-HubERT Architecture Upgrade: Upgrade the existing framework to AV-HubERT with custom architectural optimizations (such as lightweight cross-attention fusion adapters) for speaker-independent continuous text generation.",
                        "Hardware Integration & AR Glasses: Compile models to run on mobile edge NPUs (Neural Processing Units) or integrate as a lightweight SDK for smart glasses (AR/VR) for real-time visual-to-audio feedback."
                    ]
                    for i, bullet in enumerate(bullets):
                        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                        p.text = "• " + bullet
                        p.level = 0  # Fix paragraph indentation alignment
                        p.space_after = Pt(12)
                        p.font.size = Pt(16)
                        p.font.name = "Inter"

    # Slide 12: Video Solution and Github Repo
    elif idx == 12:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "Github Repo: Provide repository Link" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    
                    p0 = tf.paragraphs[0]
                    p0.text = "GitHub Repository: https://github.com/AlekhyaGangopadhyay/Lip2Speech_ReVox"
                    p0.font.size = Pt(18)
                    p0.font.bold = True
                    p0.font.name = "Outfit"
                    
                    p1 = tf.add_paragraph()
                    p1.text = "Hugging Face Space: https://huggingface.co/spaces/iamalekhya/Lip2Speech"
                    p1.font.size = Pt(18)
                    p1.font.bold = True
                    p1.font.name = "Outfit"
                    p1.space_before = Pt(20)

    # Slide 13: Conclusion & References
    elif idx == 13:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if "By implementing a well-researched" in text:
                    shape.text_frame.clear()
                    tf = shape.text_frame
                    tf.word_wrap = True
                    
                    p0 = tf.paragraphs[0]
                    p0.text = "By implementing a well-researched and innovative hybrid deep learning framework, our goal is to establish a sustainable, privacy-first, offline assistive framework for speech-impaired individuals."
                    p0.font.size = Pt(15)
                    p0.font.name = "Inter"
                    p0.space_after = Pt(24)
                    
                    p1 = tf.add_paragraph()
                    p1.text = "References:"
                    p1.font.size = Pt(16)
                    p1.font.bold = True
                    p1.font.name = "Outfit"
                    p1.space_after = Pt(6)
                    
                    refs = [
                        "1. Assael, Y. M., Shillingford, B., Whiteson, S., & de Freitas, N. (2016). LipNet: Sentence-level Lipreading.",
                        "2. Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks.",
                        "3. Cooke, M., Barker, J., Cunningham, S., & Shao, X. (2006). An audio-visual corpus for speech perception and automatic speech recognition (GRID Corpus).",
                        "4. Raffel, C., et al. (2020). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)."
                    ]
                    for ref in refs:
                        p_ref = tf.add_paragraph()
                        p_ref.text = ref
                        p_ref.font.size = Pt(12)
                        p_ref.font.name = "Inter"
                        p_ref.space_after = Pt(4)

# Save the populated presentation
prs.save(output_path)
print(f"\nSuccessfully populated presentation and saved to: {output_path}")
