with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is
   x : array(1..4,1..3) of INTEGER;
   y: INTEGER;
   z: INTEGER;
begin
    for y in 1..4
    loop
		for z in 1..3
		loop
			x(y,z):=y*z;
			Print(x(y,z));
			Print_Char(',');
		end loop;
		Print_Newline(1);
    end loop;

end Proced2;


