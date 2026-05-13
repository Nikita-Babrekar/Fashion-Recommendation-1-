document.addEventListener("DOMContentLoaded", () => {

    const mode = document.getElementById("mode");
    const manualSection = document.getElementById("manualSection");
    const imageSection = document.getElementById("imageSection");
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");

    const btn = document.getElementById("generateBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("btnSpinner");

    const resultsDiv = document.getElementById("results");
    const toneBadge = document.getElementById("toneBadge");
    const toneText = document.getElementById("detectedToneText");
    const errorBox = document.getElementById("errorBox");

    // Toggle Mode
    mode.addEventListener("change", () => {
        if (mode.value === "manual") {
            manualSection.style.display = "block";
            imageSection.style.display = "none";
        } else {
            manualSection.style.display = "none";
            imageSection.style.display = "block";
        }
    });

    // Image Preview
    imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];
        if (file) {
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        }
    });

    // Main Button
    btn.addEventListener("click", async () => {

        resultsDiv.innerHTML = "";
        errorBox.style.display = "none";
        toneBadge.style.display = "none";

        spinner.style.display = "block";
        btnText.innerText = "Processing...";
        btn.disabled = true;

        try {
            let response;

            if (mode.value === "manual") {
                const skinTone = document.getElementById("skinTone").value;
                const bodyShape = document.getElementById("bodyShape").value;

                response = await fetch("http://127.0.0.1:5000/recommend", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        skin_tone: skinTone,
                        body_shape: bodyShape
                    })
                });

            } else {
                const file = imageInput.files[0];
                if (!file) {
                    throw new Error("Upload image first");
                }

                const bodyShape = document.getElementById("bodyShape").value;

                const formData = new FormData();
                formData.append("image", file);
                formData.append("body_shape", bodyShape);

                response = await fetch("http://127.0.0.1:5000/recommend", {
                    method: "POST",
                    body: formData
                });
            }

            const data = await response.json();

            // ❌ Handle backend errors
            if (!response.ok) {
                errorBox.innerText = data.error;
                errorBox.style.display = "block";
                return;
            }

            // ❌ Handle invalid tone
            if (data.tone === "invalid") {
                errorBox.innerText = "Invalid image. Upload a real human face.";
                errorBox.style.display = "block";
                return;
            }

            // ✅ Show tone
            toneText.innerText = data.tone;
            toneBadge.style.display = "block";

            // ✅ Show results
            data.recommendations.forEach(item => {
                const div = document.createElement("div");
                div.className = "card-item";

                div.innerHTML = `
                    <img src="${item.img}" />
                    <p>${item.name}</p>
                `;

                resultsDiv.appendChild(div);
            });

        } catch (err) {
            errorBox.innerText = err.message;
            errorBox.style.display = "block";
        } finally {
            spinner.style.display = "none";
            btnText.innerText = "Generate";
            btn.disabled = false;
        }
    });

});