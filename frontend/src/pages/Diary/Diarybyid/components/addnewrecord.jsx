import { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

export const AddNewRecord = ({ exerName, exer_id }) => { 
    const [weight, setWeight] = useState("")
    const [reps, setReps] = useState("")
    const { exerID } = useParams();


    const handleNewRecord = async() => { 
        console.log({
            exer_id,
            exerName,
            weight: Number(weight),
            reps: Number(reps)
          });
        
        const response = await axios.post("http://localhost:8000/diary/add-new-record", {
            exer_id,
            exerName,
            weight,
            reps
        },{withCredentials:true}
    
    )

     }

     return(
        <>
           <form action="">
           <input
                    type="number"
                    min="1"
                    max="400"
                    step="1"
                    value={weight}
                    placeholder="súly"
                    onChange={e => setWeight(e.target.value)}
                    />
            <br />

            <input
                    type="number"
                    min="1"
                    max="20"
                    step="1"
                    value={reps}
                    placeholder="ismétlés"
                    onChange={e => setReps(e.target.value)}
                    />
                    <br />
            
            <button type="button" onClick={handleNewRecord}>Naplózás</button>

           </form>

        </>

     )



}