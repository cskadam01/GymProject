import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AddNewRecord } from "./components/addnewrecord";
import { GetDiaryDetail } from "./components/getDiaryDetails";
import api from "../../api";

export const OpenedExer = () => {
    const [exerName, setExerName] = useState("")
    const { id } = useParams();
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        
        const GetExerByID = async () => {
            setLoading(true)
            const response = await api.get(`/exercise/exer/${id}`);
            setExerName(response.data.exer_name);
            setLoading(false);
        };
        
        GetExerByID();
    }, [id]);


    if (loading) return    <p>töltés</p>

    if (error) return <p>Hibás feladat vagy nincs jogosultságod!</p>;

    return(

        <>


    

        
        <>
        <AddNewRecord exerName={exerName} exer_id={id}/>
        <GetDiaryDetail exer_id={id} onError={() => setError(true)} /> 
        </>
      
        

        </>
        
        
    )
   
    







}

