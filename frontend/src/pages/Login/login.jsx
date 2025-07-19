import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../instance";
import "./login.css"
import { Link } from "react-router-dom";



export const Login = () => {

    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const HandleLogin = async (e) => {
        try {
            const response = await axios.post("/users/login",
                {
                    name,
                    password
                },
                
                


            );
            const token = response.data.access_token
            localStorage.setItem("access_token",  token);

            navigate("/profile");
            setName("")
            setPassword("")


            console.log(response.data)



        }

        catch (err) {
            setError(err?.response?.data?.detail)




        }

    };


    return (

        <>  <div className="login-container">
            <form action="">
                <div className="login-cont">
                    <div className="login-margin">
                    <h1>Jó újra látni</h1>
                    <h2>Jelentkezz be fiókodba</h2>

                    <div className="login-tilte-error">
                    <p className="login-input-title"> Felhsználónév</p>
                    {error === "Helytelen felhasználónév" && <p className="login-error-username">{error}</p>}
                    </div>

                    <input type="text"
                        placeholder="Felhasználónév"
                        name=""
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />


                    <br />
                    <div className="login-tilte-error">
                    <p className="login-input-title">Jelszó</p>
                    {error === "Helytelen jelszó" && <p className="login-error">{error}</p>} </div>
                        <input type="password"
                    
                        placeholder="Jelszó"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <br />
                    <Link to ={"/register"} style={{textDecoration:"none"}}>
                    <p className="login-link">Még nincs Felhasználód?</p></Link>
                    <button className="login-button" type="button" onClick={HandleLogin}>Login</button>
                </div>
                
                </div>
            </form>

        </div>
        </>


    )
};