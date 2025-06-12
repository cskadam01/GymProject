import { useEffect, useState} from "react";
import axios from "axios";

export const GetDiaryDetail = ( {exer_id, refresh_key}) => {

    const [logs, setLogs] = useState([])
    const [loading, setLoading] = useState(true);
    

    useEffect(() => {
        const LoadProgression = async () => {
          try {
            const response = await axios.get(
              `http://localhost:8000/diary/by-exercise?exercise_id=${exer_id}`,
              { withCredentials: true }
            );
            setLogs(response.data);
          } catch (err) {
            if (err.response?.status === 404) {
            setLogs([])

            }
          }

          finally{
            setLoading(false)

          }
        };
      
        LoadProgression();
      }, [exer_id, refresh_key ]);

   
    
    return(
        
        logs.length === 0 ?(
            <p>Még nincs nalpó</p> 

        ):(<div>
                {logs.map((item) =>(
                    <div key={item.id}>
                        <p>{item.date}</p>
                        <p>{item.exer_name}</p>
                        <p>{item.rep}</p>
                        <p>{item.weight}</p>


                    </div>

                ))
                
                 
                }


            </div>
        )
            
    
    
    )


}