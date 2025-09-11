import { useState, useEffect } from "react"
import axios from "../../../instance"
import "./NewPassword.css"
export const NewPassword = () =>{

    const [oldPass, setOldPass] = useState("")
    const [newPass, setNewPass] = useState("")
    const [message, setMessage] = useState("")
    const [result, setResult] = useState(null)
    const [newPassCheck, setNewPassCheck] = useState("")



    const HandleNewPass = async() =>{

        if(newPass !== newPassCheck){
            setMessage("A jelszavak nem egyeznek")
            setResult(true)
            return
        }

        try{
        const response = await axios.post("/change-password", {
            old_passowrd : oldPass,
            new_password : newPass

        }

        
        )

        if (response.status === 200){
            setMessage("Jelszavad sikeresen megváltozott")
            setResult(false)

        }}
        catch (error) {
            
            const status = error.response?.status;
            
          
            if (status === 404) {
              setMessage("A megadott jelszó helytelen");
            } else if (status === 500) {
              setMessage("Szerverhiba");
            } else if (status) {
            
              setMessage(`Ismeretlen hiba (kód: ${status})`);
            } else {
              
              setMessage("Hálózati hiba vagy a szerver nem elérhető");
            }
            setResult(true)
          }
        }


return(

        <div className="new-pass-container">
            
            {result !== null && <div className={result ? "new-pass-fail" : "new-pass-success"}>{message}</div>}
         
            <div className="new-class-content">
                <p>Régi jelszavad</p>
                <input type="password"
                value={oldPass}
                onChange={(e)=> setOldPass(e.target.value)}
                />
                <p>Új jelszavad</p>
                <input type="password"
                value={newPass}
                onChange={(e)=> setNewPass(e.target.value)}
                />
                <p>Jelszó ellenörzése</p>
                <input type="password"
                value={newPassCheck}
                onChange={(e)=> setNewPassCheck(e.target.value)}
                />

                <button onClick={HandleNewPass}>Jelszó megváltoztatása</button>
                
            </div>
        </div>
    ) 

    }

           


