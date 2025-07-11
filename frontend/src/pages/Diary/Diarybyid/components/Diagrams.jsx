import { useState } from "react";
import React from "react";
import axios from "axios";
import { ConfirmDeleteModal } from "./confirm_modal/confirm";

import {
  Chart as ChartJS, //Grafiaki Monitor
  LineElement, //Maga a vonal
  PointElement, //Pontok
  CategoryScale, //X tengely típus
  LinearScale, //Y tengely típus
  Tooltip, //buborék
  Legend, //Szín Magyarázat
  defaults,
  TimeScale,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import "./getDiaryDetails.css"
import 'chartjs-adapter-date-fns';
import "./Diagram.css"


defaults.maintainAspectRatio= false;
defaults.responsive = true;


ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  TimeScale,
  PointElement,
  Filler,
  Tooltip,
  Legend
);




export const Diagrams = ({title, logs, triggerRefresh}) => {

  const [selectedLog, setSelectedLog] = useState(null);
  console.log(logs);
    return(

    <div className="diagram-container">
<Line

  data={{
    datasets: [
      {
        label: title,
        data: logs.map((item) => ({ x: new Date(item.date), y: item.weight })),
        borderColor: "#987bff",
        backgroundColor: 'hsla(260, 100%, 50%, 0.1)',
        tension: 0.5,
        fill: true
      },
    ],
  }}
  
    options={{
      // ...
      onClick: (event, elements, chart) => {
        if (elements.length > 0) {
          const chartElement = elements[0];
          const index = chartElement.index;
          const datasetIndex = chartElement.datasetIndex;
          const clickedPoint = logs[index];
          setSelectedLog(clickedPoint);

        }
        else {
          setSelectedLog(null); // <== ha nem kattintottál pontra, akkor törli
        }
      },
    scales: {
      x: {
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
        min: logs.length > 0 ? new Date(new Date(logs[0].date).getTime() - 86400000) : undefined,
        max: logs.length > 0 ? new Date(new Date(logs[logs.length - 1].date).getTime() + 86400000) : undefined,
        ticks: {
          display: false,
          color: "",
          maxRotation: 45,
          minRotation: 45
        },
        grid: {
          color: "#202026"
        },
        title: {
          display: false,
          text: "Dátum ",
          color: "",
          font: {
            weight: "bold",
            size: 15
          }
        }
      },
      y: {
        ticks: {
          color: "969393",
        },
        grid: {
          color: "#202026"
        },
        max:
          logs.length > 0
            ? Math.ceil(Math.max(...logs.map(l => l.weight)) / 10) * 10 + 10
            : undefined
      }
    },
    elements: {
      line: {
        tension: 0.5
      }
    }
  }}
/>

<ConfirmDeleteModal
  selectedLog={selectedLog}
  onCancel={() => setSelectedLog(null)}
  onConfirm={() => {
    axios
    axios
    .delete(`http://localhost:8000/diary/delete/${selectedLog.id}`, {
      withCredentials: true,
    })
      .then(() => {
        alert("Sikeresen törölve");
        setSelectedLog(null);
        triggerRefresh(); 
      });
  }}
/>



    
    
 

   

</div>
    )

};














