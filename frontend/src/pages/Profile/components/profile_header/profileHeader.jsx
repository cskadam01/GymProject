import { VscAccount } from "react-icons/vsc";
import style from "./profileHeader.module.css"



export  function ProfileHeader({username}) {
    return(
        <>
               <div className={style["prof-head-container"]}>
                          {/* glow */}
                        <div
                            className={style.glow}
                            style={{ background:"#3f0ca6" }}
                        />

                    <div className={style["prof-head-cont"]}>
                        <div style={{display:"flex"}}>
                        <VscAccount style={{ color:"#3f0ca6", marginTop:"3%", fontWeight:"bold", fontSize:"3rem"}}/>
                        <div>
                        <h5>Üdv</h5>
                        <h4> {username}!</h4>

                        </div>
                       
                        </div>
                      
                       <p>Kövesd nyomon az edzésedet és érd el a célod a FluxNote segítségével. Tarts ki, minden edzes számít!</p>

                    </div>

               </div>
            
        </>


    )
}