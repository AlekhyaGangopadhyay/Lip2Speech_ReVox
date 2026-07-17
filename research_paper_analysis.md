# Lip2Speech Research Paper Review & Proposed Modifications

This document contains a comprehensive analysis of the research paper [Lip2Speech-Research Paper(5).pdf](file:///d:/Lip2Speech_Final/lip2speech/Lip2Speech-Research%20Paper(5).pdf) alongside the training and inference pipeline defined in the Jupyter notebook [revoxfinaltry.ipynb](file:///d:/Lip2Speech_Final/lip2speech/revoxfinaltry.ipynb). 

---

## 1. Suggested Corrections & Improvements for the Paper

### Title and Abstract
* **Title Typo**: Change `"Spacio-Temporal"` to `"Spatio-Temporal"` in the title.
* **Abstract Grammar**:
  * *Current*: `"...this work delivers a integrated offline system, presents an assistive communication system..."`
  * *Correction*: `"...this work delivers an integrated offline system, presenting an assistive communication system..."`

### Section I: Introduction
* **Grammar / Flow**:
  * *Current*: `"This research develops a proposed system takes a silent video..."`
  * *Correction*: `"This research presents a system that takes a silent video..."`
  * *Current*: `"Therefore, lip-reading has numerous application ranging from..."`
  * *Correction*: `"Therefore, lip-reading has numerous applications ranging from..."`
* **Terminology**: Introduce the concept of **Visemes** (visual representations of phonemes) when describing the ambiguities of phonemes in lip motion (e.g., how "p", "b", and "m" look identical on the lips).
* **Section I-B (Applications)**:
  * *Current*: `"...with person who has lost their voice..."` $\rightarrow$ `"...with a person who has lost their voice..."`
  * *Current*: `"Speech also more instantaneous..."` $\rightarrow$ `"Speech is also more instantaneous..."`
  * *Current*: `"...in forensic investigation Lip2Speech is applied..."` $\rightarrow$ `"...in forensic investigations, Lip2Speech can be applied..."`
  * *Current*: `"...speech of their silent..."` $\rightarrow$ `"...speech from their silent..."`

### Section II: Literature Review
* **Spacing and Typos**:
  * Fix word runs like `"movementshas"` $\rightarrow$ `"movements has"`, `"ill-posednature"` $\rightarrow$ `"ill-posed nature"`, `"movementsitself"` $\rightarrow$ `"movements itself"`, `"needsto"` $\rightarrow$ `"needs to"`, and `"usingdatasets"` $\rightarrow$ `"using datasets"`.
  * Fix missing space: `"prosody.Therefore"` $\rightarrow$ `"prosody. Therefore"`.
* **Subsection (e) - T5 Model Description**:
  * Remove the prefix `"Book:"` from `"Book: T5 (0.75B~3B):"`. It appears to be an artifact of copied text. Change to: `"T5 (0.75B to 3B parameters):..."`
* **Subsection (f) - Punctuation**:
  * Change `". [4]."` to `". [4]"` or `"[4]."` at the end of the sentence.

### Section III: Research Gap & Contributions
* **Academic Tone**:
  * *Current*: `"...it is very clear to current models where they fail to produce clear outputs. But if we divide our work in two parts, it is easier to achieve the model."`
  * *Correction*: `"Existing end-to-end models often struggle to produce intelligible acoustic outputs directly from silent video. By decoupling the task into two sub-problems—lip-to-text decoding followed by text-to-speech synthesis—we leverage robust linguistic priors and achieve highly accurate and natural results."`
* **Voice Customization Claim**:
  * The paper states: `"First, we would like to clearly state that our goal is to be able to generate speech from a silent lip video of any speaker and in any desired target voice."`
  * *Note*: The code implementation uses standard offline text-to-speech engines (`pyttsx3`/`gTTS`) which synthesize speech in a single voice. To be accurate, clarify that the current system synthesizes speech in a standardized assistive voice, and highlight voice cloning/zero-shot transfer as a future scope.

### Section IV-A: System Architecture
* **Video Duration Limitation**:
  * Explain that the system slices videos up to $25$ frames ($1.0$ second at $25$ FPS) to keep CPU inference times low. For continuous speech, mention that a sliding window approach can be used.
* **Haar Cascade vs. Modern Face Detectors**:
  * Briefly state that while OpenCV Haar Cascades are preferred for low-latency CPU inference, they are sensitive to extreme head rotations, and modern CNN-based face/landmark models could be swapped in for high-power target devices.

### Section V: Results & Discussion
* **Formatting Typos**:
  * Change `"82.3to 93.6"` to `"82.3% to 93.6%"`.
  * Change `"8.5to 3.2"` to `"8.5% to 3.2%"`.
* **Ablation Study Description**:
  * In **Table II**, the Baseline uses a partially frozen MobileNetV2 (layers 0–13 frozen, 14–18 unfrozen) and Ablation A uses a 100% unfrozen CNN. Table II lists Baseline as `"Frozen MobileNetV2"`. It should be updated to `"Partially Frozen MobileNetV2 (Blocks 14+ Unfrozen)"` to match the actual implementation.

---

## 2. Rigorous Mathematical Methodology Section

Below is the structured, LaTeX-formatted mathematical formulation of your Lip2Speech system. This section should be inserted under **Section IV (Proposed Methodology)** in your paper.

### Proposed Methodology Formulation

The proposed Lip2Speech framework translates a sequence of silent video frames into refined speech through a decoupled three-stage pipeline: **Spatial-Temporal Lip Reading**, **Language Model Post-Processing**, and **Assistive Speech Synthesis**.

#### A. Video Preprocessing and Region of Interest (ROI) Extraction
Let the input video $V$ be a sequence of $T$ RGB frames:
$$V = \{f_1, f_2, \dots, f_T\}, \quad f_t \in \mathbb{R}^{H \times W \times 3}$$

where $T$ represents the temporal context size ($T = 25$). For each frame $f_t$, a Haar Cascade classifier extracts the face bounding box $(x_t, y_t, w_t, h_t)$. The lower facial region containing the mouth is cropped and normalized using the transformation $g_{\text{crop}}$ and resized to $112 \times 112$ pixels via $g_{\text{resize}}$:
$$X_t = g_{\text{resize}}\left(g_{\text{crop}}(f_t)\right) \in \mathbb{R}^{112 \times 112 \times 3}$$

The normalized sequence of mouth crops is denoted by $X = \{X_1, X_2, \dots, X_T\}$.

#### B. Spatial Feature Extraction (MobileNetV2)
A 2D MobileNetV2 architecture, pre-trained on ImageNet, functions as the spatial feature extractor. To adapt the features from generic images to mouth contours and lip shapes, the final convolutional blocks (blocks 14 to 18) are unfrozen and fine-tuned, while the earlier layers remain frozen. 

Let $f_{\text{CNN}}(\cdot; \theta_{\text{CNN}})$ represent the feature extraction layers of MobileNetV2 parameterized by weights $\theta_{\text{CNN}}$. For each frame $t$, the output feature map is passed through global average pooling (GAP) to generate a $1280$-dimensional spatial descriptor:
$$z_t = \text{GAP}\left(f_{\text{CNN}}(X_t; \theta_{\text{CNN}})\right) \in \mathbb{R}^{1280}$$

This yields the sequence $Z = \{z_1, z_2, \dots, z_T\} \in \mathbb{R}^{T \times 1280}$.

#### C. Temporal Sequence Modeling (Bidirectional LSTM)
To capture the bidirectional temporal dependencies and co-articulation effects inherent in continuous lip movement, the spatial sequence $Z$ is fed into a 2-layer Bidirectional LSTM (BiLSTM). 

For each timestep $t \in \{1, 2, \dots, T\}$, the forward and backward hidden states are computed as:
$$\vec{h}_t = \text{LSTM}_{\text{forward}}\left(z_t, \vec{h}_{t-1}, c_{t-1}^{\text{forward}}; \theta_{\text{forward}}\right)$$
$$\overleftarrow{h}_t = \text{LSTM}_{\text{backward}}\left(z_t, \overleftarrow{h}_{t+1}, c_{t+1}^{\text{backward}}; \theta_{\text{backward}}\right)$$

The standard LSTM cell gating equations at each timestep are governed by:
$$\begin{aligned}
i_t &= \sigma\left(W_i z_t + U_i h_{t-1} + b_i\right) \\
f_t &= \sigma\left(W_f z_t + U_f h_{t-1} + b_f\right) \\
o_t &= \sigma\left(W_o z_t + U_o h_{t-1} + b_o\right) \\
\tilde{c}_t &= \tanh\left(W_c z_t + U_c h_{t-1} + b_c\right) \\
c_t &= f_t \odot c_{t-1} + i_t \odot \tilde{c}_t \\
h_t &= o_t \odot \tanh(c_t)
\end{aligned}$$

where $\sigma(x) = \frac{1}{1 + e^{-x}}$ is the sigmoid activation function, $\odot$ represents the Hadamard (element-wise) product, $W_*$ and $U_*$ are weight matrices, and $b_*$ are bias vectors.

The temporal state representation $h_t^{\text{temp}}$ at timestep $t$ is the concatenation of both directional hidden states:
$$h_t^{\text{temp}} = \left[\vec{h}_t \,\|\, \overleftarrow{h}_t\right] \in \mathbb{R}^{2 \cdot d_{\text{hidden}}}$$

where $d_{\text{hidden}} = 256$ is the hidden size of each directional LSTM layer, resulting in $h_t^{\text{temp}} \in \mathbb{R}^{512}$, and $\|$ represents the vector concatenation operator.

#### D. Word Classification and Sequence Decoding
A Fully Connected (FC) projection layer projects the temporal representation $h_t^{\text{temp}}$ to the vocabulary space. Let $V_{\text{vocab}} = 51$ be the size of the GRID Corpus vocabulary. The vocabulary logit vector at timestep $t$ is:
$$o_t = W_y h_t^{\text{temp}} + b_y \in \mathbb{R}^{V_{\text{vocab}}}$$

where $W_y \in \mathbb{R}^{V_{\text{vocab}} \times 512}$ and $b_y \in \mathbb{R}^{V_{\text{vocab}}}$. The probability of predicting the word index $k \in \{0, 1, \dots, V_{\text{vocab}}-1\}$ at timestep $t$ is given by:
$$p_t(k) = \frac{e^{o_{t,k}}}{\sum_{j=0}^{V_{\text{vocab}}-1} e^{o_{t,j}}}$$

During training, the ground truth word sequence $Y = (y_1, y_2, \dots, y_M)$ ($M \le T$) is padded with the silence token `"sil"` (index $0$) to match the temporal dimension $T$:
$$y^*_t = \begin{cases} 
      y_t & \text{if } t \le M \\
      0 & \text{if } t > M 
   \end{cases}$$

The network is trained end-to-end minimizing the categorical cross-entropy loss over all frames:
$$\mathcal{L} = -\frac{1}{T} \sum_{t=1}^{T} \log p_t(y^*_t)$$

#### E. Greedy Temporal Collapse & Language Model Refinement
During inference, a greedy decoder predicts the word index at each frame:
$$\hat{y}_t = \arg\max_{k \in \{0, \dots, V_{\text{vocab}}-1\}} p_t(k)$$

To remove duplicate predictions across consecutive frames and eliminate silence padding, a temporal collapse function is applied:
$$S_{\text{raw}} = \text{collapse}\left(\{ \hat{y}_t \mid \hat{y}_t \neq 0, t = 1, \dots, T\}\right)$$

Specifically, the collapse operator removes any token $\hat{y}_t$ if it is identical to $\hat{y}_{t-1}$. 

To correct spelling and grammar shifts caused by visual homophenes (different words with similar mouth shapes), the raw sequence $S_{\text{raw}}$ is combined with an instruction prefix:
$$\text{Prompt} = \text{"Correct the grammar and spelling: "} \mathbin{+} S_{\text{raw}}$$

Let $U = (u_1, u_2, \dots, u_L)$ be the tokenized representation of the Prompt. The local T5 decoder generates the final token sequence $S_{\text{refined}}$ by maximizing the conditional sequence probability:
$$S_{\text{refined}} = \arg\max_{W} \prod_{i=1}^{K} P_{\text{T5}}(w_i \mid w_{<i}, U)$$

where $W = (w_1, w_2, \dots, w_K)$ is the output token sequence.

#### F. Assistive Speech Synthesis
The final refined sentence $S_{\text{refined}}$ is processed by an offline Text-to-Speech (TTS) engine:
$$\text{Audio Waveform} = \text{TTS}\left(S_{\text{refined}}\right)$$

This delivers a natural, auditory representation of the user's silent lip movement.
