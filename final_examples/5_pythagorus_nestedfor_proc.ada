with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is

   i1,i2,i3 : Integer;
   x:Integer;
	procedure isPythagorean(a,b,c:in Integer; output:out Integer) is
	begin
		if a * a + b * b = c * c 
		then
			output:=1;
		else
			output:=0;
		end if;
		Print_Newline(0);
	end isPythagorean;
begin
	for i1 in 1..20
	loop
		for i2 in i1..20
		loop
			for i3 in i2..20
			loop
				isPythagorean(i1,i2,i3,x);
				if x=1
				then
					Print(i1);
					Print_Char(',');
					Print(i2);
					Print_Char(',');
					Print(i3);
					
					
					Print_Newline(1);
				end if;
				Print_Newline(0);
				
			end loop;
		end loop;
	end loop;
end Proced2;
