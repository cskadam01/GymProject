import { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import "./addnewrecord.css"

export const AddNewRecord = ({ exerName, exer_id, triggerRefresh}) => { 
    const [weight, setWeight] = useState("")
    const [reps, setReps] = useState("")
    


    const handleNewRecord = async(e) => {
         e.preventDefault();
        try{
        const response = await axios.post("http://localhost:8000/diary/add-new-record", {
            exer_id,
            exerName,
            weight,
            reps
        },{withCredentials:true}
    
    )

    triggerRefresh()
    setWeight("");
    setReps("");
    
    }

    catch(err){
        alert("nem várt hiba")
    }



     }

     return(
        <>

        <div className="add-record-container">
           <form onSubmit={handleNewRecord}>
           <input
                    type="number"
                    min="1"
                    max="400"
                    step="1"
                    value={weight}
                    placeholder="súly"
                    onChange={e => setWeight(e.target.value)}
                    />
            

            <input
                    type="number"
                    min="1"
                    max="20"
                    step="1"
                    value={reps}
                    placeholder="ismétlés"
                    onChange={e => setReps(e.target.value)}
                    />
                  
            
            <button type="submit" >Naplózás</button>
           
           </form>
        </div>
        </>

     )



}