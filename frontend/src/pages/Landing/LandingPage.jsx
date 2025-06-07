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
                <h1>FluxNote</h1>
                
                <p>Maximalizáld edzéseid egyszerűen</p>
                <Link to={"/register"}>
                <button >Vágjunk Bele</button>
                </Link>
            </div>
        </div>


        </>

    )


};
