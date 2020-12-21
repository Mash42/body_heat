CREATE TABLE `TBL_STUDENT_COMMENTS` (  
`STUDENT_ID` int(3) NOT NULL COMMENT '生徒ID',
`LABO_ID` int(3) NOT NULL COMMENT '研究室ID',
`YEAR` int(4) NOT NULL COMMENT '年度',
`COMMENTS` text DEFAULT NULL COMMENT '感想',
PRIMARY KEY (`STUDENT_ID`,`LABO_ID`,`YEAR`)) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;