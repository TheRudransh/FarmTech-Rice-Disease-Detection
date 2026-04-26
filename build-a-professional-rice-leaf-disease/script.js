const API_URL = "http://localhost:8080/predict";

const uploadForm = document.querySelector("#uploadForm");
const imageInput = document.querySelector("#imageInput");
const dropzone = document.querySelector("#dropzone");
const previewWrap = document.querySelector("#previewWrap");
const previewImage = document.querySelector("#previewImage");
const fileName = document.querySelector("#fileName");
const fileSize = document.querySelector("#fileSize");
const submitButton = document.querySelector("#submitButton");
const resetButton = document.querySelector("#resetButton");
const statusMessage = document.querySelector("#statusMessage");
const resultsPanel = document.querySelector("#resultsPanel");
const diseaseName = document.querySelector("#diseaseName");
const severityBadge = document.querySelector("#severityBadge");
const confidenceValue = document.querySelector("#confidenceValue");
const confidenceBar = document.querySelector("#confidenceBar");
const preventionList = document.querySelector("#preventionList");
const probabilityChart = document.querySelector("#probabilityChart");

let selectedFile = null;
let previewUrl = null;

const formatLabel = (value = "") =>
  String(value)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

const clampPercent = (value) => {
  const number = Number(value);
  if (Number.isNaN(number)) return 0;
  return Math.max(0, Math.min(100, number));
};

const formatPercent = (value) => `${clampPercent(value).toFixed(1)}%`;

const setStatus = (message, type = "default") => {
  statusMessage.textContent = message;
  statusMessage.classList.toggle("error", type === "error");
};

const setSelectedFile = (file) => {
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    setStatus("Please choose an image file.", "error");
    return;
  }

  selectedFile = file;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);

  previewImage.src = previewUrl;
  fileName.textContent = file.name;
  fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
  previewWrap.hidden = false;
  submitButton.disabled = false;
  resetButton.disabled = false;
  resultsPanel.hidden = true;
  setStatus("Image ready for analysis.");
};

const resetUpload = () => {
  selectedFile = null;
  imageInput.value = "";
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  previewImage.removeAttribute("src");
  previewWrap.hidden = true;
  submitButton.disabled = true;
  resetButton.disabled = true;
  resultsPanel.hidden = true;
  setStatus("");
};

const renderPrevention = (steps = []) => {
  preventionList.innerHTML = "";

  const safeSteps = Array.isArray(steps) && steps.length
    ? steps
    : ["Monitor the field regularly and consult a crop specialist for targeted treatment."];

  safeSteps.forEach((step) => {
    const item = document.createElement("li");
    item.textContent = step;
    preventionList.appendChild(item);
  });
};

const renderProbabilities = (probabilities = {}) => {
  probabilityChart.innerHTML = "";

  Object.entries(probabilities)
    .sort((a, b) => Number(b[1]) - Number(a[1]))
    .forEach(([name, value]) => {
      const percent = clampPercent(value);
      const row = document.createElement("div");
      const label = document.createElement("span");
      const track = document.createElement("div");
      const fill = document.createElement("span");
      const numericValue = document.createElement("span");

      row.className = "probability-item";
      label.className = "probability-name";
      label.textContent = formatLabel(name);
      track.className = "probability-track";
      track.setAttribute("aria-hidden", "true");
      numericValue.className = "probability-value";
      numericValue.textContent = `${percent.toFixed(1)}%`;
      track.appendChild(fill);
      row.append(label, track, numericValue);

      probabilityChart.appendChild(row);
      requestAnimationFrame(() => {
        fill.style.width = `${percent}%`;
      });
    });
};

const renderResults = (data) => {
  const severity = formatLabel(data.severity || "Low");
  const severityClass = severity.toLowerCase();
  const confidence = clampPercent(data.confidence);

  diseaseName.textContent = formatLabel(data.disease || "Unknown");
  severityBadge.textContent = severity;
  severityBadge.className = `severity-badge ${severityClass}`;
  confidenceValue.textContent = formatPercent(confidence);
  confidenceBar.style.width = "0%";

  renderPrevention(data.prevention);
  renderProbabilities(data.probabilities || {});

  resultsPanel.hidden = false;
  requestAnimationFrame(() => {
    confidenceBar.style.width = `${confidence}%`;
  });
};

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("dragover");
  setSelectedFile(event.dataTransfer.files[0]);
});

dropzone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    imageInput.click();
  }
});

imageInput.addEventListener("change", (event) => {
  setSelectedFile(event.target.files[0]);
});

resetButton.addEventListener("click", resetUpload);

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!selectedFile) {
    setStatus("Select an image before analysis.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("image", selectedFile);

  submitButton.disabled = true;
  setStatus("Analyzing image...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Prediction failed with status ${response.status}`);
    }

    const data = await response.json();
    renderResults(data);
    setStatus("Analysis complete.");
  } catch (error) {
    resultsPanel.hidden = true;
    setStatus(
      `${error.message}. Confirm the prediction server is running at ${API_URL}.`,
      "error"
    );
  } finally {
    submitButton.disabled = false;
  }
});
