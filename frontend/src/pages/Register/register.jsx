import { useState } from "react";
import api from "../api";


export const Register = () => {
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState('');
    const [passwordCheck, setPasswordCheck] = useState('');
    const [error, setError] = useState('');




    const HandleRegister = async() => {
      const response = await api.post("/users/register", {
            name,
            password,
            email,
            age
        });
        
    };



    return(

        <>
        <form action="">
            <input type="text"
            value={name}
            onChange={(e)=>setName(e.target.value)}
            placeholder="Felhasználónév"
            required/>
            <br />

            <input type="text"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            placeholder="Email"
            required/>
            <br />

            <input type="text"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            placeholder="Jelszó"
            required/>
            <br />
            
            <input type="text"
            value={passwordCheck}
            onChange={(e)=>setPasswordCheck(e.target.value)}
            placeholder="Jelszó ismétlés"
            required/>
            <br />

            <input type="text"
            value={age}
            onChange={(e)=>setAge(e.target.value)}
            placeholder="Kor"
            required/>
             <br />

            <button type="button" onClick={HandleRegister}>Regisztrácó</button>


        </form>

        </>
    )
 
};
