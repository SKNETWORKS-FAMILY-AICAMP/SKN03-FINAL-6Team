import React from "react";
import "./SecondSection.css";
import carImage from "../../../assets/images/Car1.png";

const SecondSection = ({ stage }) => {
  return (
    <div className={`second-section ${stage === 1 ? "closing" : stage === 2 ? "opening" : ""}`}>
      <div className="elevator left" style={{ backgroundImage: `url(${carImage})` }} />
      <div className="elevator right" style={{ backgroundImage: `url(${carImage})` }} />
    </div>
  );
};

export default SecondSection;
