import { useEffect, useState} from "react";
import axios from "axios";
import {
  Chart as ChartJS, //Grafiaki Monitor
  LineElement, //Maga a vonal
  PointElement, //Pontok
  CategoryScale, //X tengely típus
  LinearScale, //Y tengely típus
  Tooltip, //buborék
  Legend //Szín Magyarázat
} from 'chart.js';
import { Line } from 'react-chartjs-2';


ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
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


 
      


  const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleString('hu-HU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });

const chartData = {
  datasets: [
    {
      label: 'Súly (kg)',
      data: logs.map((item) => ({
        x: formatDate(item.date), // emberi olvasható dátum + idő
        y: item.weight,
        rep: item.rep,
      })),
      borderColor: 'rgb(223, 223, 223)',
      backgroundColor: 'rgb(43, 43, 43)',
      tension: 0.3,
      pointRadius: 5,
      pointHoverRadius: 7,
    }
  ]
};

   
    
    return(
        
        logs.length === 0 ?(
            <p>Még nincs nalpó</p> 

        ):(  <div style={{ maxWidth: '600px', margin: '2rem auto' }}>
    <Line
      data={chartData}
      options={{
        responsive: true,
        plugins: {
          tooltip: {
            callbacks: {
              // Ez fut le, ha ráviszed az egeret egy pontra
              label: function (context) {
                const rep = context.raw.rep; // a 'rep' mező az adatobjektumból
                const weight = context.raw.y;
                return `Súly: ${weight} kg – Ismétlés: ${rep}x`;
              }
            }
          },
          legend: {
            labels: {
              color: '#333', // szövegszín (opcionális)
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 10, // pl. 10 kilónként
            },
            title: {
              display: true,
              text: 'Súly (kg)'
            }
          },
                      x: {
              title: {
                display: true,
                text: 'Dátum és időpont'
              },
              ticks: {
                maxRotation: 45,
                minRotation: 45,
                autoSkip: false
              }
            }

        }
      }}
    />
  </div>

        )
            
    
    
    )


}