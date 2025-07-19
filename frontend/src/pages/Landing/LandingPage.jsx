import { Link } from "react-router-dom";
import "./LandingPage.css"




export const LandingPage = () => {
    return (
        <><div className="landing-container">
            <div>
                <Link to={"/login"}>
                <button className="landing-login">Bejelentkezés</button>
                </Link>
            </div>
            <div className="landing-cont">
                <h1 style={{color:""}}>FluxNote</h1>
                
                <h2 style={{color:""}}>Maximalizáld edzéseid egyszerűen</h2>
                
                
                <Link to={"/register"}>
                <button >Vágjunk Bele</button>
                </Link>
            </div>
        </div>


        </>

    )


};
