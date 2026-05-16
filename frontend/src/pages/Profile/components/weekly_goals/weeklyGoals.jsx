import style from "./weeklyGoals.module.css";
import React from "react";
import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);


const centerTextPlugin = {
  id: "centerText",
  afterDraw(chart) {
    const { ctx, chartArea } = chart;
    if (!chartArea) return;

    const x = (chartArea.left + chartArea.right) / 2;
    const y = (chartArea.top + chartArea.bottom) / 2;

    const ds = chart.data.datasets?.[0];
    const current = ds?.__current ?? 0;
    const goal = ds?.__goal ?? 0;

    ctx.save();
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    ctx.font = "600 28px system-ui";
    ctx.fillStyle = "#ffffff";
    ctx.fillText(`${current}/${goal}`, x, y - 6);

    ctx.font = "500 12px system-ui";
    ctx.fillStyle = "rgba(255,255,255,0.7)";
    ctx.fillText("edzes", x, y + 18);

    ctx.restore();
  },
};

function WeekDots({ days = [] }) {
  const labels = ["H", "K", "Sze", "Cs", "P", "Szo", "V"];

  // Support two inputs:
  // 1) ["H","K","Sz"] day-label array
  // 2) [true,false,...] boolean array (length 7)
  let safe;
  if (Array.isArray(days) && days.length === 7 && typeof days[0] === "boolean") {
    safe = Array.from({ length: 7 }, (_, i) => Boolean(days[i]));
  } else {
    const daySet = new Set((days || []).map((d) => String(d)));
    safe = labels.map((lab) => daySet.has(lab));
  }

  return (
    <div style={{ display: "flex", gap: 14, justifyContent: "center", marginTop: 14 }}>
      {labels.map((d, i) => (
        <div key={d + i} style={{ textAlign: "center" }}>
          <div style={{ fontSize: 12, color: "rgba(255,255,255,0.6)" }}>{d}</div>
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: 999,
              margin: "6px auto 0",
              background: safe[i] ? "#3f0ca6" : "rgba(255,255,255,0.12)",
            }}
          />
        </div>
      ))}
    </div>
  );
}

export const WeeklyGoal = ({
  current,
  goal,
  days,
}) => {
  if (!current) {
    return (
      <div className={style.weeklyGoalCard}>
        <h3>Heti cél</h3>
        <div style={{ opacity: 0.6, textAlign: "center", marginTop: 20 }}>
          <p style={{color: "#9AA0B4"}}>még nincs kitűzött cél</p>
        </div>
      </div>
    );
  }

  const safeGoal = Math.max(1, Number(goal) || 1);
  const safeCurrent = Math.min(Math.max(0, Number(current) || 0), safeGoal);
  const remaining = safeGoal - safeCurrent;

  const data = {
    labels: ["done", "remaining"],
    datasets: [
      {
        data: [safeCurrent, remaining],
        backgroundColor: ["#3f0ca6", "rgba(255,255,255,0.12)"],
        borderWidth: 0,
        cutout: "75%",
        __current: safeCurrent,
        __goal: safeGoal,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    rotation: -90,
    circumference: 360,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  };

  return (
    <div className={style.weeklyGoalCard}>
        <h3>Heti cél</h3>

      <div style={{ width: 220, height: 220, margin: "18px auto 0" }}>
        <Doughnut data={data} options={options} plugins={[centerTextPlugin]} />
      </div>

      <WeekDots days={days} />
    </div>
  );
};