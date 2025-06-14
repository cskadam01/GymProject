import { useState } from "react";
import axios from "axios";
import "./navbar.css"
import { Link } from 'react-router-dom';
import { RxHamburgerMenu } from "react-icons/rx";


export const Navbar =() => {

    const [isOpen, setIsOpen] = useState(false);

   
        const HandleLogout = async () => {
        try{
        const response = await axios.post("http://localhost:8000/users/logout", {}, {withCredentials: true});
        

        console.log("kijelentkezve:",response.data);
    
        }
        catch (err){
            console.error(error)


    }};


     const OpenNavbar = () => {
            setIsOpen(!isOpen)
           
        };





    return(

        <>
        <nav className="navbar-container">
            <div className="navbar">
            <div className="top">
                <h1>FluxNote</h1>
                <button onClick={OpenNavbar}><RxHamburgerMenu /></button>
            </div>

            <ul className={`menu ${isOpen ? 'open' : ''}`}>
                <li><Link style={{textDecoration:"none"}} to="/profile"><p className="nav-routes">Profilom</p></Link></li>
                <hr />
                <li><Link style={{textDecoration:"none"}} to="/diary"><p className="nav-routes">Naplóm</p></Link></li>
                <hr />
                <li><Link style={{textDecoration:"none"}} to="/browse-exercises"><p className="nav-routes">Elérhető feladatok</p></Link></li>
                <hr />

                <li><button onClick={HandleLogout}>Kijelentkezés</button></li>
            </ul>
            </div>
        </nav>
        </>
    )



}



