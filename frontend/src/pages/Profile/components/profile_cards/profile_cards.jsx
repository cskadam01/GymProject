import { RxBorderSolid } from "react-icons/rx"
import style from "./profile_cards.module.css"

export function ProfileCard({ name, number, text, icon, borderColor, backGroundColor, glowColor }) {
  return (
    <div
      className={style.container}
      style={{
        background: backGroundColor,
        borderColor: borderColor,
      }}
    >
      {/* glow */}
      <div
        className={style.glow}
        style={{ background: glowColor || borderColor }}
      />

      <div className={style.content}>
        <div className={style.left}>
          <p style={{ marginBottom: "10%", color: "#9AA0B4" }}>{name}</p>
          <p style={{ color: "#D6D9E6", marginBottom: "15%" }}>{number}</p>
          <p style={{ color: "#9AA0B4", fontSize: "0.7rem" }}>{text}</p>
        </div>

        <div className={style.right}>
          {icon}
        </div>
      </div>
    </div>
  );
}
