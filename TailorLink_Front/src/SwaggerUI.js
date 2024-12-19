import React from "react";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";

const SwaggerComponent = () => {
  return (
    <SwaggerUI url="http://dkwcdr.iptime.org:8000/docs" />
  );
};

export default SwaggerComponent;
