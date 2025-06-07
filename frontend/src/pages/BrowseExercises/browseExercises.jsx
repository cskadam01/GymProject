import { useState, useEffect} from "react";
import api from "../../api";


export const BrowseExercises = () => {
    const [exercises, setExercises] = useState([])
    const [error, setError] = useState("")
    const [res, setRes] = useState("")
    
    

    useEffect(() =>{
        const GetAllExercise = async () =>{
            try{
                const response = await api.get("/exercise/get-all-exercise")
                if (response.status == 200){
                    setExercises(response.data)
                    console.log("Adatok eltárolva", exercises)
                }
            }
            catch(err){
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
        try{
            const response = await api.post("/exercise/save-to-diary",{
                exerciseID
            })
            if(response.status === 200){
                setRes("Feladat sikeresen hozzá adva a naplódhoz")
            }
        }

        catch (err){
            setError("Valami hiba lépett fel a naplózás során")

        }
        
    }
      

    return(
        <>

            <>
            {exercises.map((exercise, index) => (
                <div key={index}>
                    <h3>{exercise.exer_name}</h3>
                    <p>Izomcsoport: {exercise.muscle}</p>
                    <p>Típus: {exercise.type}</p>
                    <p>Leírás: {exercise.exer_description}</p>
                    <p>Elmentve: {exercise.saved ? "✅ Igen" : "❌ Nem"}</p>
                    <button onClick={() => addToDiary(exercise.id)}>+</button>

                    <hr />
                </div>
            ))}
</>
        
        </>



    )



}