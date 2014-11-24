--insertion sort within main program

with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is
   Item  : array(1..20) of INTEGER;
   First : INTEGER := 1;
   Last  : INTEGER := 20;
   Value : INTEGER;
   J     : INTEGER;
   I	 : INTEGER;
begin
	
	--assign values inside array
	for I in 1..20
	loop
		Item(I):=20-I;
		Item(I):=Item(I)-2+14*9/3;
		Print(Item(I));
		Print_Char(',');
	end loop;
	Print_Newline(1);
	
	   for I in 2..20 
	   loop
	      Value := Item(I);
	      J := I - 1;
	      while J >= 1 and Item(J) > Value 
	      loop
		Item(J + 1) := Item(J);
		J := J - 1;
	      end loop;
	      Item(J + 1) := Value;
	      --Print(Item(J+1));
	      --Print_Newline(1);
   end loop;
	for I in 1..20
	loop
		Print(Item(I));
		Print_Char(',');
	end  loop;

end Proced2;
