import { useEffect, useState} from "react";
import axios from "../../../../instance";
import { Diagrams } from "./Diagrams";
import {
  Chart as ChartJS, //Grafiaki Monitor
  LineElement, //Maga a vonal
  PointElement, //Pontok
  CategoryScale, //X tengely típus
  LinearScale, //Y tengely típus
  Tooltip, //buborék
  Legend, //Szín Magyarázat
  defaults,
  TimeScale
} from 'chart.js';

import "./getDiaryDetails.css"
import 'chartjs-adapter-date-fns';


defaults.maintainAspectRatio= false;
defaults.responsive = true;


ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  TimeScale,
  PointElement,
  Tooltip,
  Legend
);

export const GetDiaryDetail = ( {exer_id, refresh_key}) => {

    const [logs, setLogs] = useState([])
    const [loading, setLoading] = useState(true);
    

    useEffect(() => {
        const LoadProgression = async () => {
          try {
            const response = await axios.get(
              `/diary/by-exercise?exercise_id=${exer_id}`,
              
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
      const groupedLogs = {
        "pr": logs.filter((item) => item.rep <= 2),
        "3-4": logs.filter((item) => item.rep === 3 || item.rep === 4),
        "5-6": logs.filter((item) => item.rep === 6 || item.rep === 5),
        "7-8": logs.filter((item) => item.rep === 8 || item.rep === 7),
        "9-10": logs.filter((item) => item.rep === 9 || item.rep === 10),
        "11 +": logs.filter((item) => item.rep >= 11),
      };

    return(
        
        logs.length === 0 ?(
            <p style={{color:"white"}}>Még nincs nalpó</p> 

        ):( 

            //----------------------Diagram Komponensek Létrehozása Ismétlésszám Alapján ----------------------
           <div className="exer-diagram">
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>1 Ismétléses Rekord</h1>
            <Diagrams title = "PR" logs={groupedLogs["pr"] } triggerRefresh={() => setRefreshKey(prev => prev + 1)}  />
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>3-4 közti ismétlés tartomány</h1>
            <Diagrams title = "3-4 ismétlés közt" logs={groupedLogs["3-4"]} triggerRefresh={() => setRefreshKey(prev => prev + 1)} />
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>5-6 közti ismétlés tartomány</h1>
            <Diagrams  title = "5-6 ismétlés közt" logs={groupedLogs["5-6"]} triggerRefresh={() => setRefreshKey(prev => prev + 1)} />
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>7-8 közti ismétlés tartomány</h1>
            <Diagrams  title = "7-8 ismétlés közt" logs={groupedLogs["7-8"]} triggerRefresh={() => setRefreshKey(prev => prev + 1)} />
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>9-10 közti ismétlés tartomány</h1>
            <Diagrams  title = "9-10 ismétlés közt" logs={groupedLogs["9-10"]} triggerRefresh={() => setRefreshKey(prev => prev + 1)} />
            <h1 style={{color:'white', marginBottom:'30px', fontSize:'1.6rem', marginLeft:'5%'}}>11 és a feletti ismétlés tartomány</h1>
            <Diagrams  title = "11-nél Több ismétlés" logs={groupedLogs["11 +"]} triggerRefresh={() => setRefreshKey(prev => prev + 1)} />
            </div>

        )
    )
}