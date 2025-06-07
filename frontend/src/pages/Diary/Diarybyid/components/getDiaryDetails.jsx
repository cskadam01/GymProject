import { use, useEffect, useState, useTransition } from "react";
import api from "../../../api";

export const GetDiaryDetail = ( {exer_id, onError}) => {

    const [logs, setLogs] = useState([])
    const [localError, setLocalError] = useState(false);

    useEffect(() => {
        const LoadProgression = async () => {
          try {
            const response = await api.get(
              `/diary/by-exercise?exercise_id=${exer_id}`
            );
            setLogs(response.data);
          } catch (err) {
            if (err.response?.status === 404) {
              onError();
              setLocalError(true)
            }
          }
        };
      
        LoadProgression();
      }, [exer_id, onError]);

    if (localError) return null

    return(
        <>
            <div>
                {logs.map((item) =>(
                    <div key={item.task_id}>
                        <p>{item.date}</p>
                        <p>{item.exer_name}</p>
                        <p>{item.rep}</p>
                        <p>{item.weight}</p>


                    </div>

                ))
                
                 
                }


            </div>
        
        </>

    )


}