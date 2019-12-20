rule TFG_Ibrahi_Alejandro{

	strings:
		$a = "TFG"
		$b = "Ibrahi"
		$c = "Alejandro"
		
	condition:
		$a and $b and $c
	}