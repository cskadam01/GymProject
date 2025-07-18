import axios from "../../instance";
import { useEffect, useState } from "react";
import { Navbar } from "../../Navbar/navbar";
import "./BrowseExercises.css"



export const BrowseExercises = () => {
    const [exercises, setExercises] = useState([])
    const [error, setError] = useState("")
    const [res, setRes] = useState("")




    useEffect(() => {
        const GetAllExercise = async () => {
            try {
                const response = await axios.get("/exercise/get-all-exercise",
                   
                )
                if (response.status == 200) {
                    setExercises(response.data)
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

                <div className="exer-cont">
                {exercises.map((exercise, index) => (
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