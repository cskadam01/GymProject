import axios from "../../instance";
import { useEffect, useState } from "react";
import { Navbar } from "../../Navbar/navbar";
import "./BrowseExercises.css"



export const BrowseExercises = () => {
    const [exercises, setExercises] = useState([])
    const [error, setError] = useState("")
    const [res, setRes] = useState("")
    const [selectedMuscles, setSelectedMuscles] = useState([]);
    const muscleGroups = ["Váll", "Hát", "Mell", "Bicepsz","Tricepsz", "Láb"]; // legyenek nagybetűvel, ahogy az adatbázisban van





    useEffect(() => {
        const GetAllExercise = async () => {

            const timestamp = localStorage.getItem("all_exercises_timestamp");
            const now = Date.now();
        
            // Ha kevesebb mint 1 óra telt el (1 óra = 1000 * 60 * 60 ms)
            if (timestamp && now - parseInt(timestamp) < 1000 * 60 * 60) {
              const cached = localStorage.getItem("all_exercises");
              if (cached) {
                const parsed = JSON.parse(cached);
                setExercises(parsed);
                console.log("Feladatok betöltve localStorage-ből");
                return;
              }
            }

            try {
                const response = await axios.get("/exercise/get-all-exercise",
                   
                )
                if (response.status == 200) {
                    setExercises(response.data)
                    localStorage.setItem("all_exercises", JSON.stringify(response.data));
                    console.log("Adatok eltárolva", exercises)
                }
            }
            catch (err) {
                console.log("Hiba: ", err.response.data.detail)

            }
        }
        GetAllExercise();
    }, []);

    // Ez a useffect azért kell hogy tudjuk figyelni amikor változik az exercise tömb akkor frissüljön az oldal is, mivel az előzőben még nem frissül
    useEffect(() => {
        console.log("Exercisek frissültek:", exercises);
    }, [exercises]); //ebbe a tömbbe kell írni a figyelni kívánt objektumot, aminek a változásakor frissül a render


    const addToDiary = async (exerciseID) => {
        try {
            const response = await axios.post("https://gymproject-gpdz.onrender.com/diary/save-to-diary", {
                exerciseID
            },
                {
                    withCredentials: true
                }

            )
            if (response.status === 200) {
                setRes("Feladat sikeresen hozzá adva a naplódhoz")
                alert("Feladat hozzá adva naplóhoz")
            }
        }

        catch (err) {
            setError("Valami hiba lépett fel a naplózás során")

        }

    }


    return (
        <>
            


            <div className="exer-container">
            <Navbar/>
            <div style={{ padding: "10px", color: "white", display: "flex", flexWrap: "wrap", gap: "15px" }}>
                {muscleGroups.map((muscle) => (
                    <label key={muscle}>
                    <input
                        type="checkbox"
                        checked={selectedMuscles.includes(muscle)}
                        onChange={() =>
                        setSelectedMuscles((prev) =>
                            prev.includes(muscle)
                            ? prev.filter((m) => m !== muscle)
                            : [...prev, muscle]
                        )
                        }
                    />
                    {muscle}
                    </label>
                ))}
                </div>

                <div className="exer-cont">
                {exercises
                        .filter((exercise) =>
                            selectedMuscles.length === 0 || selectedMuscles.includes(exercise.muscle)
                        )
                        .map((exercise, index) => (
                    <div className="exer-list"key={index}>

                        <h3 className="browse-name">{exercise.exer_name}</h3>
                        <p  className="browse-muscle">Izomcsoport: {exercise.muscle}</p>
                        <p  className="browse-type">Típus: {exercise.type}</p>
                        <p  className="browse-desc">Leírás: {exercise.exer_description}</p>
                        <p  className="browse-isSaved">{exercise.saved ? "Ez a feladat már szerepel a naplódban" : null}</p>
                        {exercise.saved ? <button className="exer-button-dis" disabled>Hozzáadás</button> : <button className="exer-button-active" onClick={() => addToDiary(exercise.id)}>Hozzáadás</button>  }
                        

                        
                    </div>
                ))}
            </div>
        </div>     
        </>



    )



}