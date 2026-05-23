async function predictDisease(){

    const checkedSymptoms =

        document.querySelectorAll(
            ".symptom-checkbox:checked"
        );

    let symptoms = [];

    checkedSymptoms.forEach((item)=>{

        symptoms.push(item.value);

    });

    // VALIDATION

    if(symptoms.length === 0){

        alert("Please select symptoms");

        return;
    }

    try{

        const response = await fetch("/predict", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                symptoms:symptoms
            })

        });

        const data = await response.json();

        console.log(data);

        // HANDLE ERRORS

        if(data.error){

            alert(data.error);

            return;
        }

        const resultCard =

            document.getElementById(
                "result-card"
            );

        let topPredictionsHTML = "";

        data.top_predictions.forEach((item)=>{

            topPredictionsHTML += `

                <li>

                    ${item.disease}
                    -
                    ${item.confidence}%

                </li>

            `;
        });

        resultCard.innerHTML = `

            <div class="dashboard-card">

                <h2>
                    ${data.prediction.disease}
                </h2>

                <h3>
                    Confidence:
                    ${data.prediction.confidence}%
                </h3>

                <div class="progress-bar">

                    <div
                        class="progress-fill"
                        style="
                        width:${data.prediction.confidence}%
                        ">
                    </div>

                </div>

                <h3 style="margin-top:20px;">

                    Top Predictions

                </h3>

                <ul>

                    ${topPredictionsHTML}

                </ul>

                <a href="/precautions/${data.prediction.disease}">

                    <button>

                        View Precautions

                    </button>

                </a>

            </div>

        `;

    }

    catch(error){

        console.log(error);

        alert("Prediction failed");

    }
}