import { useState, useEffect} from "react";
import axios from "../../instance";
import "./ForgotPass.css"

export const ForgotPass = () => {
    const [name, setName] = useState("");
    const [message, setMessage] = useState("")
    const [success, setSuccess] = useState(null)
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        if(success !== null ){
            const timer = setTimeout(()=>{
                setSuccess(null)
            
            }, 5000)

        }

    },[success])


    const handleEmailSend = async() => {
        setSuccess(null)
        setMessage("")
        setIsLoading(true)
        

        if (name === "") {
            setMessage("Mező kitöltése kötelező")
            setSuccess(false)
            setIsLoading(false)
            return
        }

        try{const response = await axios.post("/users/forgotten-passoword",{user_name : name});

        if (response.status == 200){
            setIsLoading(false)
            setMessage("Az új jelszavad elküldtük az emailedre")
            setSuccess(true);
            setName("")

        } }

        catch(error){
            if (error.response.status == 404){
                setMessage("Nem található email cím.")


            }
            else if (error.response.status == 500){
                setMessage("Szerver hiba áll fent, jelenleg nem tudunk emailt küldeni.")
            }
            else{
                setMessage("Ismeretlen hiba lépett fel")

            }
            setIsLoading(false)
            setSuccess(false);


        }
    }
   

    return (
        <>
            <div className="forgot-container">
            { success!== null && (<div className={success ? "forgot-success" : "forgot-fail"}> {message} </div>)


} 
                <div  className="forgot-content">
                    

                    

                    <h3>Elfelejett jelszó</h3>

                    <input type="text"
                    placeholder="Felhasználónév"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    
                    />

                    <p>Add meg a felhasználóneved,<p></p> és elküldjük az új jelszavad</p>
                    <button onClick={handleEmailSend}>Új jelszó kérése</button>
                    {isLoading &&  <div className="forgot-loading"> <p>Email küldése folyamatban...</p></div>}



                </div>
            </div>
        
        </>
    )
}