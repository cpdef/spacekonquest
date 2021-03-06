unit uPlanet;

{$mode objfpc}{$H+}

interface

uses
  FileUtil, Forms, Controls, Graphics, Dialogs, StdCtrls,
  Classes, SysUtils, uSpaceship;

type
TPlanet = class
 owner, production, ships, kill_percent, x, y: integer;
 color: tcolor;
 name: string;
 function send_ships(nr: integer; target:TPlanet): TSpaceship;
 procedure turn_start(player_on_turn: integer);
 procedure touch_down(nr, effective, player: integer);
 constructor create(newowner, tx, ty:integer; home_planet: boolean);
 procedure new_name();
 procedure new_color();
end;

implementation

function TPlanet.send_ships(nr: integer; target:TPlanet): TSpaceship;
begin
end;

procedure TPlanet.turn_start(player_on_turn: integer);
begin
  if player_on_turn = owner then ships := ships+production;
end;

procedure TPlanet.touch_down(nr, effective, player: integer);
begin
end;

procedure TPlanet.new_name();
var len, i: integer;
    new_char: string;
begin
   name := '';
   len := 1+random(7);
   for i:=0 to len do begin
       new_char := chr(ord('0')+random(10));
       if random(2) = 1 then new_char := chr(ord('A')+random(26));
       //showmessage(new_char);
       name := name+new_char;
   end;
end;

procedure TPlanet.new_color();
var cRed, cGreen, cBlue: integer;
begin
   repeat
   cRed:=56+Random(200);
   cGreen:=56+Random(200);
   cBlue:=56+Random(200);
   until abs(cRed-cGreen) > 100;
   color:=RGBToColor(cRed, cGreen, cBlue);
end;

constructor TPlanet.create(newowner, tx, ty:integer; home_planet: boolean);
begin
  owner := newowner;
  x := tx;
  y := ty;
  ships := 0;
  if home_planet then begin
      production := 10;
      kill_percent := 7;
  end
  else begin
      production := 7+random(8);
      kill_percent := 5+random(6);
  end;
  new_name();
  new_color();
  //if owner = 0 then showmessage('no owner')
  //else showmessage('owner');
  //showmessage(inttostr(production)+';'+inttostr(kill_percent)+';'+name);
end;

end.

