
const audioInput = document.getElementById("audioFile");
const analyzeBtn = document.getElementById("analyzeBtn");

const fileName = document.getElementById("fileName");
const loading = document.getElementById("loading");
const result = document.getElementById("result");


// FILE SELECTION
audioInput.addEventListener("change", () => {

    fileName.textContent = audioInput.files.length
        ? audioInput.files[0].name
        : "No file selected";

});


// ANALYZE AUDIO
analyzeBtn.addEventListener("click", async () => {

    if (!audioInput.files.length) {
        alert("Please select an audio file.");
        return;
    }

    const formData = new FormData();

    formData.append("audio", audioInput.files[0]);

    analyzeBtn.disabled = true;

    loading.textContent =
        "AI model is analysing your recording...";

    result.classList.add("hidden");

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok || data.status === "error") {
            throw new Error(
                data.error || data.message || "Analysis failed."
            );
        }


        // DISPLAY PREDICTION
        const prediction =
            document.getElementById("prediction");

        prediction.textContent = data.prediction;

        document.getElementById("resultMessage").textContent =
            data.message;


        // DYNAMIC RESULT ICON
        const resultIcon =
            document.getElementById("resultIcon");

        const predictionText =
            String(data.prediction || "").toLowerCase();

        if (predictionText.includes("ai-generated")) {

            resultIcon.textContent = "⚠️";
            resultIcon.style.color = "#f59e0b";

        } else if (predictionText.includes("human")) {

            resultIcon.textContent = "✓";
            resultIcon.style.color = "#00f477";

        } else {

            resultIcon.textContent = "ℹ";
            resultIcon.style.color = "#94a3b8";

        }


        // AUDIO METRICS
        document.getElementById("duration").textContent =
            data.duration + " seconds";

        document.getElementById("centroid").textContent =
            data.spectral_centroid + " Hz";


        // CONFIDENCE SCORES
        const fakeScore =
            document.getElementById("fakeScore");

        const realScore =
            document.getElementById("realScore");

        const fakeBar =
            document.getElementById("fakeBar");

        const realBar =
            document.getElementById("realBar");


        if (data.fake_score !== null &&
            data.fake_score !== undefined) {

            const fakePercentage =
                data.fake_score * 100;

            fakeScore.textContent =
                fakePercentage.toFixed(2) + "%";

            fakeBar.style.width =
                Math.max(0, Math.min(100, fakePercentage)) + "%";

        } else {

            fakeScore.textContent = "Unmapped";
            fakeBar.style.width = "0%";

        }


        if (data.real_score !== null &&
            data.real_score !== undefined) {

            const realPercentage =
                data.real_score * 100;

            realScore.textContent =
                realPercentage.toFixed(2) + "%";

            realBar.style.width =
                Math.max(0, Math.min(100, realPercentage)) + "%";

        } else {

            realScore.textContent = "Unmapped";
            realBar.style.width = "0%";

        }


        // RAW MODEL OUTPUT
        document.getElementById("rawOutput").textContent =
            JSON.stringify(data.raw_predictions, null, 2);


        // SHOW REPORT
        result.classList.remove("hidden");


    } catch (error) {

        alert("Error: " + error.message);

    } finally {

        analyzeBtn.disabled = false;
        loading.textContent = "";

    }

});


const videoInput = document.getElementById("videoFile");
const videoFileName = document.getElementById("videoFileName");
const videoAnalyzeBtn = document.getElementById("videoAnalyzeBtn");
const videoStatus = document.getElementById("videoStatus");

videoInput.addEventListener("change", () => {
    videoFileName.textContent = videoInput.files.length
        ? videoInput.files[0].name
        : "No video selected";

    videoStatus.textContent = "";
});


videoAnalyzeBtn.addEventListener("click", async () => {

    if (!videoInput.files.length) {
        alert("Please select a video first.");
        return;
    }

    const formData = new FormData();
    formData.append("video", videoInput.files[0]);

    videoAnalyzeBtn.disabled = true;
    videoStatus.textContent = "Extracting video frames...";

    const videoResults = document.getElementById("videoResults");

    videoResults.classList.add("hidden");

    try {
        const response = await fetch("/analyze-video", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Video analysis failed.");
        }

        document.getElementById("videoResultStatus").textContent =
            "Frames extracted successfully";

        document.getElementById("totalFrames").textContent =
            data.total_frames;

        document.getElementById("extractedFrames").textContent =
            data.extracted_frames;

        videoResults.classList.remove("hidden");
        videoStatus.textContent = "Video processing completed!";

    } catch (error) {
        videoStatus.textContent = "Error: " + error.message;

    } finally {
        videoAnalyzeBtn.disabled = false;
    }
});

       
const viewHistoryBtn = document.getElementById("viewHistoryBtn");
const historyResults = document.getElementById("historyResults");
const historyList = document.getElementById("historyList");

viewHistoryBtn.addEventListener("click", async () => {
    viewHistoryBtn.disabled = true;
    viewHistoryBtn.textContent = "Loading...";

    try {
        const response = await fetch("/history-data");
        const records = await response.json();

        historyList.innerHTML = "";

        if (records.length === 0) {
            historyList.textContent = "No analysis history available.";
        } else {
            records.forEach(record => {
                const item = document.createElement("div");
                item.className = "history-item";

                item.innerHTML = `
                    <h4>${record.filename}</h4>
                    <p>Type: ${record.media_type}</p>
                    <p>Result: ${record.prediction}</p>
                    <p>Date: ${record.created_at}</p>
                `;

                historyList.appendChild(item);
            });
        }

        historyResults.classList.remove("hidden");

    } catch (error) {
        historyList.textContent = "Unable to load history.";
        historyResults.classList.remove("hidden");

    } finally {
        viewHistoryBtn.disabled = false;
        viewHistoryBtn.textContent = "View History";
    }
});
