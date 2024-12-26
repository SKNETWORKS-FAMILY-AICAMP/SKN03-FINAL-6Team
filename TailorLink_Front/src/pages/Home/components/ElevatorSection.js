import React from "react";
import "./ElevatorSection.css";
import carImage from "../../../assets/images/Car1.png";

const ElevatorSection = ({ stage }) => {
  return (
    <div className={`elevator-section ${stage === 1 ? "closing" : stage === 2 ? "opening" : ""}`}>
      <div className="elevator left" style={{ backgroundImage: `url(${carImage})` }}></div>
      <div className="elevator right" style={{ backgroundImage: `url(${carImage})` }}></div>
    </div>
  );
};

export default ElevatorSection;
