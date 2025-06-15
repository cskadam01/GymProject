import { useEffect, useState} from "react";
import axios from "axios";
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
import { Line } from 'react-chartjs-2';
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

      const groupedLogs = {
        3: logs.filter((item) => item.rep === 3),
        6: logs.filter((item) => item.rep === 6),
        8: logs.filter((item) => item.rep === 8),
        12: logs.filter((item) => item.rep === 12),
      };


 
      


 


   
    
    return(
        
        logs.length === 0 ?(
            <p>Még nincs nalpó</p> 

        ):(  <div className="exer-diagram">
    
 <Line
 data={{
   datasets: [
     {
       label: "Súly 6 ismétlésnél",
       data: groupedLogs[6].map(item => ({ x: item.date, y: item.weight })),
       borderColor: "#00bcd4",
       backgroundColor: "#00bcd4"
     }
   ]
 }}

      options = {{
        scales: {
          x:{
            type: 'time',
            time: {
                unit: "day",
                tooltipFormat: "yyyy-MM-dd HH:mm",
                displayFormats: {
                  minute: "HH:mm",
                  hour: "MMM d HH:mm",
                  day: "yyyy-MM-dd"

                }

            },
            ticks:{
              color: "969393",
              maxRotation: 90,
              minRotation: 70,
            },
            grid: {
              color:"#303030"
            },
            title:{
              display: true,
              text: "Dátum ",
              color:"969393",
              font :{
                weight: "bold",
                size: "15"

              }


            }
          },
          y: {
            ticks: {
              color: "969393"


            },
            grid: {
              color: "#303030"
            }

          }


        },
        elements: {
          line: {
            tension: 0.3

          }

        }

      }}
    />
  </div>

        )
            
    
    
    )


}