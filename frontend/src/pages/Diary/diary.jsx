import { useState, useEffect } from "react";
import axios from "../../instance";
import { Link } from "react-router-dom";
import "./diary.css"
import { Navbar } from "../../Navbar/navbar";
import { RxGear } from "react-icons/rx";
import { CgGym } from "react-icons/cg";


export const Diary = () => {
    const [diary, setDiary] = useState([])
    const [selectedMuscles, setSelectedMuscles] = useState([]);
    const muscleGroups = ["Váll", "Hát", "Mell", "Bicepsz","Tricepsz", "Láb"];

    

    const handleCheckboxChange = (muscle) => {
        setSelectedMuscles((prev) =>
          prev.includes(muscle)
            ? prev.filter((m) => m !== muscle)
            : [...prev, muscle]
        );
      };
 
    useEffect(() => {
        const getUserDiary = async () => {
            try {
               

                const response = await axios.get("/diary/user-diary",
                )

                setDiary(response.data)

            }

            catch (err) {


            }
        }
        getUserDiary()

    }, [])

    return (
        <>  
            <Navbar/>
            <div className="diary-conatiner">
            <div style={{ padding: "10px", color: "white" }}>
                {muscleGroups.map((muscle) => (
                    <label key={muscle} style={{ marginRight: "10px" }}>
                    <input
                        type="checkbox"
                        checked={selectedMuscles.includes(muscle)}
                        onChange={() => handleCheckboxChange(muscle)}
                    />
                    {muscle}
                    </label>
                ))}
                </div>

                <div className="diary-cont" style={{paddingBottom:"20px"}}>
                {diary.length === 0 ? (
                    <p style={{color:"white"}}>Napló üres</p>             

                ) : (
                    diary
                            .filter((item) =>
                                selectedMuscles.length === 0 || selectedMuscles.includes(item.muscle)
                            )
                            .map((item) => (
                        <div className="diary-item" key={item.id} >
                            
                            <Link to={`/diary/${item.id}`} style={{textDecoration:"none"}}>   {/* Beadjuk, hogy a választott linkre vigye tovább a felhasználót az id alapján */}
                                <div className="diary-data">
                                <p className="diary-data-name">{item.exer_name}</p>
                                <p className="diary-data-muscle">{item.muscle}</p>
                                {item.type === "Szabadsúly" ? <p className="diary-icon"><CgGym /></p> : <p className="diary-icon"><RxGear /></p>}
                                
                                <br />
                                </div>
                            </Link>
                        </div>

                    )

                    ))

                }</div>
            </div>
        </>

    )
}