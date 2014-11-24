with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is

   Counter : INTEGER:=6;
   Counter2 : INTEGER:=1;
   Counter3 : INTEGER:=5;
   
	procedure Fact(x : in Integer; result :out Integer) is
	   temp : INTEGER;
	   begin
		--Print(x);
		if x>1 then
			Fact(x-1, result);
			result:=result*x;
			--Print(result);
		else
			result:=x;
		end if;
		--Print(result);
		x:=1;
	   end Fact;


begin
   Print(Counter2);
   Print_Newline(1);
   Fact(Counter,Counter2);
   Print(Counter2);
   
end Proced2;
