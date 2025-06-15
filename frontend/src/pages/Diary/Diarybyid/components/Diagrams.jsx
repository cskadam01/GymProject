import { useState } from "react";
import React from "react";
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
import "./Diagram.css"


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




export const Diagrams = ({title, logs}) => {

    return(

    <div className="diagram-container">
    <Line
       
      
        data={{
          datasets: [
            {
              label: title,
              data: logs.map((item) => ({ x: new Date(item.date), y: item.weight })),
              borderColor: "#b0b0b0",
              backgroundColor: "#1a1a1a",
              tension: 0.5,
            },
          ],
        }}

         options={{
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
       
            min: logs.length > 0 ? new Date(new Date(logs[0].date).getTime() - 86400000) : undefined, // -1 nap
            max: logs.length > 0 ? new Date(new Date(logs[logs.length - 1].date).getTime() + 86400000) : undefined, // +1 nap
        
        ticks: {
        autoSkip: false,
          callback: function(value, index, values) {
            const date = this.getLabelForValue(value);
            return date; // mutatja az összeset
  },
          color: "969393",
          maxRotation: 45,
          minRotation: 45
        },
        grid: {
          color: "#303030"
        },
        title: {
          display: true,
          text: "Dátum ",
          color: "969393",
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
          color: "#303030"
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

    
    
 

   

</div>
    )

};














