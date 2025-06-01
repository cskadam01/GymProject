import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";



export const Login = () => {

    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [email, setemail] = useState('');
    const [age, setAge] = useState('');
    const navigate = useNavigate();

    const HandleLogin = async(e) => {
        try{
            const response = await axios.post("http://localhost:8000/users/login",
                {
                    name,
                    password
                },
                {
                    withCredentials: true
                }


            );
            navigate("/profile");

            console.log(response.data)



        }

        catch(err){



        }
        
    };


    return(

    <>  
        <form action="">
            
            <input type="text"
            placeholder="Felhasználónév"
            name=""
            value={name}
            onChange={(e) => setName(e.target.value)} 
            required
            />
            <br />


            <input type="text"
            placeholder="Jelszó"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required 

            
            />
            <br />

            <button type="button" onClick={HandleLogin}>Login</button>

        </form>


    </>


    )
};