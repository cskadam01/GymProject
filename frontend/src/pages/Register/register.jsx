import { useState } from "react";
import "./register.css"
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import axios from "../../instance";


export const Register = () => {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState('');
    const [passwordCheck, setPasswordCheck] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [disabled, setDisabled] = useState(false);




    const HandleRegister = async () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{6,}$/
        

        if (!emailRegex.test(email)) {
        setError("Nem megfelelő formátum");
        return;
        }

        
        if (password !== passwordCheck) {
            setError("Jelszavak nem egyeznek")
            return
        }


        if(!passwordRegex.test(password)){
            setError("A jelszónak legalább 6 karakter hosszúnak kell lennie, és tartalmaznia kell számot és nagybetűt")
            return
        }

        setTimeout(() => setDisabled(false), 5000);
        setDisabled(true);
        


            try {
                const response = await axios.post("/users/register",

                    {
                        name,
                        password,
                        email,
                        age
                    },
                    {
                        withCredentials: true
                    }


                );
                setError("")
                navigate("/login");


            }
            catch (err) {
                const status = err?.response?.status;

                if(status === 409){
                setError(err?.response?.data?.detail || "ismeretlen hiba")
                setName("")    
            }
                else if(status === 422){
                setError("Hiányzó adatok")
                }
                else{
                setError("Ismeretlen hiba történt");
                }

            }
        
      
    }

    const CheckEmail = () => {
        const emaiCheck = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emaiCheck.test(email)){
            return ("Hibás felhasunálónév")
        }
    };





    return (

        <>
            <div className="register-container">
                <div className="register-cont">
                    <h1>Regisztráció</h1>
                    {(error === "Hiányzó adatok" || error === "Ismeretlen hiba történt") && (
                    <p className="register-top-error">{error}</p>
                    )}
                    <div className="register-title-cont">
                        <p className="register-title">Felhasználónév</p>
                        {error == "Foglalt felhasználónév" && <p id="register-name-error">{error}</p>}
                    </div>


                    <form action="">
                        <input type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Felhasználónév"
                            required />
                        <br />


                        <div className="register-title-cont">
                        <p className="register-title">Email</p>
                        {error == "Nem megfelelő formátum" && <p id="register-pass-error">{error}</p>}
                        </div>
                        <input type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="példa@valami.com"
                            required />
                        <br />

                        <div className="register-title-cont">
                            <p className="register-title">Jelszó</p>
                            {error == "A jelszavak nem egyeznek" && <p id="register-pass-error">{error}</p>}

                        </div>
                        {error == "A jelszónak legalább 6 karakter hosszúnak kell lennie, és tartalmaznia kell számot és nagybetűt" && <p id="register-pass-long">{error}</p>}
                        <input type="text"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Jelszó"
                            required />
                        <br />

                        <p className="register-title">Jelszó ismétlés</p>
                        <input type="text"
                            value={passwordCheck}
                            onChange={(e) => setPasswordCheck(e.target.value)}
                            placeholder="Jelszó ismétlés"
                            required />
                        <br />


                        <p className="register-title">Kor</p>
                        <input type="number"
                            min="1"
                            max="100"
                            value={age}
                            onChange={(e) => setAge(e.target.value)}
                            placeholder="Kor"
                            required />
                        <br />
                        <Link to={"/login"} style={{textDecoration:"none"}}>
                            <p className="register-link">Már Van fiókod?</p>
                        </Link>


                        <button type="button" onClick={HandleRegister} disabled={disabled}>
                        Regisztráció
                        </button>




                    </form> </div>
            </div>
        </>
    )

};