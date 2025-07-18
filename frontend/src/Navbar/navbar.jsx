import { useState } from "react";
import axios from "axios";
import "./navbar.css"
import { Link } from 'react-router-dom';
import { RxHamburgerMenu } from "react-icons/rx";
import { useNavigate } from "react-router-dom";


export const Navbar =() => {

    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate()

   
        const HandleLogout = async () => {
            localStorage.removeItem("access_token")
            navigate("/login")
        }

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



