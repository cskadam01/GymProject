import { useState, useEffect} from "react";
import axios from "axios";


export const BrowseExercises = () => {
    const [exercises, setExercises] = useState([])
    

    useEffect(() =>{
        const GetAllExercise = async () =>{

            try{
                const response = await axios.get("http://localhost:8000/exercise/get-all-exercise")

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
      

    return(
        <>
       
            <p>{exercises}</p>
        
        </>



    )



}