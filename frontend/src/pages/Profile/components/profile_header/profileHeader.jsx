import { VscAccount } from "react-icons/vsc";
import "./profileHeader.css"



export  function ProfileHeader({username}) {
    return(
        <>
               <div className="prof-head-container">
                    <div className="prof-head-cont">
                       <VscAccount style={{ color:"#3f0ca6", marginTop:"2px"}}/>
                       <p>Üdv {username} !</p>

                    </div>

               </div>
            
        </>


    )
}