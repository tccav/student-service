DO
$$

		-- populate students
		INSERT INTO students (id, name, cpf, birth_date, email, course_id)
		VALUES (201320509912, 'Liz Sophie Moreira', '79715568700', '1993-01-18', 'lizsm@ol.com', 'f5be09bc-0711-11ee-be56-0242ac120002'),
			   (201520103310, 'José Raimundo da Luz', '99386241978', '1990-05-11', 'luz_joser@ol.com', 'f5be09bc-0711-11ee-be56-0242ac120002'),
			   (201810601511, 'Kamilly Sophie Mariana Baptista', '36192126518', '1998-08-25', 'ksbaptista@ol.com', 'f5be09bc-0711-11ee-be56-0242ac120002');
		COMMIT;
	END;
$$