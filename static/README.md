# Lip2Speech Paper Visualization Assets Directory

This folder contains the graphical figures, diagrams, and dashboards for the Lip2Speech system. Below is a guide detailing the purpose of each asset, its target section in an IEEE format paper, and its recommended caption.

---

### 1. Training & Validation Curves (`loss_accuracy_curves.png`)
* **What it is**: Dual-pane plot showing Cross-Entropy Loss (train vs. validation) and Validation Accuracy over 15 training epochs.
* **Relative Link**: [loss_accuracy_curves.png](loss_accuracy_curves.png)
* **Target Section**: **Section V (Results and Discussion)**, immediately after introducing the validation split setup.
* **IEEE Caption**: 
  ```latex
  \begin{figure}[htbp]
  \centerline{\includegraphics[width=\linewidth]{static/loss_accuracy_curves.png}}
  \caption{Training and validation loss curves (left) alongside validation accuracy curves (right) over 15 training epochs on the GRID dataset. The graphs demonstrate a steady convergence of loss and stable performance scaling up to 82.3\% validation accuracy.}
  \label{fig:loss_accuracy_curves}
  \end{figure}
  ```

---

### 2. Ablation Study Trade-offs (`ablation_study_chart.png`)
* **What it is**: Dual-axis bar chart comparing epoch compute latency (seconds) against training loss for the Baseline model, Ablation A (100% unfrozen CNN), and Ablation B (10-frame context drop).
* **Relative Link**: [ablation_study_chart.png](ablation_study_chart.png)
* **Target Section**: **Section V-A (Data Analysis)**, placed near **Table II (Ablation Study Matrix)**.
* **IEEE Caption**: 
  ```latex
  \begin{figure}[htbp]
  \centerline{\includegraphics[width=\linewidth]{static/ablation_study_chart.png}}
  \caption{Computational and performance trade-offs across different ablation configurations. The left y-axis (blue) highlights the epoch latency in seconds, while the right y-axis (red) details the final training loss, illustrating the selection of Baseline (Layer 14+ Unfreeze) as the optimal balance for real-time edge execution.}
  \label{fig:ablation_study_chart}
  \end{figure}
  ```

---

### 3. T5 Language Model Enhancement (`t5_enhancement_chart.png`)
* **What it is**: Side-by-side bar chart showing the comparison of Word Accuracy Rate (WAR) and Character Error Rate (CER) before and after using the local T5 post-processing LLM.
* **Relative Link**: [t5_enhancement_chart.png](t5_enhancement_chart.png)
* **Target Section**: **Section IV-G (Local Language Model-Based Post-processing)** or **Section V (Results and Discussion)**.
* **IEEE Caption**: 
  ```latex
  \begin{figure}[htbp]
  \centerline{\includegraphics[width=\linewidth]{static/t5_enhancement_chart.png}}
  \caption{Visual word accuracy rate (WAR) and character error rate (CER) comparisons before and after applying the local T5 LLM corrector, illustrating a substantial drop in error rate and correction of visually ambiguous tokens.}
  \label{fig:t5_enhancement}
  \end{figure}
  ```

---

### 4. End-to-End System Architecture (`system_architecture.png` / `novelty_flowchart.png`)
* **What it is**: High-resolution diagrams outlining the step-by-step pipeline of face tracking, mouth ROI extraction, spatial-temporal classification (MobileNetV2-BiLSTM), greedy decoding, LLM-based post-correction, and speech synthesis.
* **Relative Links**: 
  * [system_architecture.png](system_architecture.png)
  * [novelty_flowchart.png](novelty_flowchart.png)
* **Target Section**: **Section IV (Proposed Methodology)**, right at the beginning of the section.
* **IEEE Caption**: 
  ```latex
  \begin{figure}[htbp]
  \centerline{\includegraphics[width=\linewidth]{static/system_architecture.png}}
  \caption{End-to-end architecture of the proposed Lip2Speech framework illustrating the sequential pipeline of video acquisition, face detection, mouth ROI extraction, MobileNetV2-based spatial feature extraction, BiLSTM temporal sequence modeling, greedy decoding, T5-based language refinement, and offline speech synthesis.}
  \label{fig:system_architecture}
  \end{figure}
  ```
