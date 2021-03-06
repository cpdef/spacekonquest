unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, FileUtil, Forms, Controls, Graphics, Dialogs, StdCtrls,
  ExtCtrls, Buttons, uPlanet, uSpaceship, uPlayer;

type

  { TForm1 }

  TForm1 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    Button4: TButton;
    Button5: TButton;
    Button6: TButton;
    Edit1: TEdit;
    Image1: TImage;
    Label1: TLabel;
    Label2: TLabel;
    DEBUGLABEL: TLabel;
    Infolabel: TLabel;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button4Click(Sender: TObject);
    procedure Button5Click(Sender: TObject);
    procedure Button6Click(Sender: TObject);
    procedure Edit1KeyPress(Sender: TObject; var Key: char);
    procedure FormCreate(Sender: TObject);
    procedure Image1Click(Sender: TObject);
  private
    { private declarations }
  public
    { public declarations }
  end;

  TGame = class
   ships: array of TSpaceship;
   map: array of array of integer;
   planets: array of TPlanet;
   players: array of TPlayer;
   constructor create(nx, ny, new_player_nr, planet_nr: integer);
   procedure next_player();
   procedure click_on_screen(x, y:integer);
   procedure refresh_screen();
   procedure set_startplanet(planet_id:integer);
   procedure set_targetplanet(planet_id:integer);
   procedure reset_labels();
   function send(nr: integer): boolean;
   function get_planet_info(planet_id, player: integer): string;
   private
   turn, player_on_turn, zoom, startplanet, targetplanet, player_nr, x, y: integer;
  end;

var
  Form1: TForm1;
  game: Tgame;
const
  sLineBreak = {$IFDEF LINUX} AnsiChar(#10) {$ENDIF}
               {$IFDEF MSWINDOWS} AnsiString(#13#10) {$ENDIF};

implementation

{$R *.lfm}

{ TForm1 }

//////////////FORM1
procedure TForm1.Button1Click(Sender: TObject);
begin
   game := Tgame.create(30, 30, 2, 15);
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
   game.next_player();
end;

procedure TForm1.Edit1KeyPress(Sender: TObject; var Key: Char);
begin
  // #8 is Backspace
  if not (Key in [#8, '0'..'9']) then begin
    // Discard the key
    Key := #0;
  end;
end;

procedure TForm1.Button3Click(Sender: TObject);
begin
   if edit1.text <> '' then game.send(strtoint(edit1.text));
end;

procedure TForm1.Button4Click(Sender: TObject);
begin
  game.reset_labels();
  game.refresh_screen();
end;

procedure TForm1.Button5Click(Sender: TObject);
begin
    if (((game.zoom+1)*game.x) < 750) and (((game.zoom+1)*game.y) < 500)
        then game.zoom := game.zoom+1;
    game.refresh_screen();
end;

procedure TForm1.Button6Click(Sender: TObject);
begin
    if game.zoom > 3 then game.zoom := game.zoom-1;
    game.refresh_screen();
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  game := Tgame.create(20, 20, 2, 15);
end;

procedure TForm1.Image1Click(Sender: TObject);
var pt: tpoint;
begin
   pt := Mouse.CursorPos;
   pt := Image1.ScreenToClient(pt);
   game.click_on_screen(pt.x, pt.y);
end;

//////////////GAME
procedure Tgame.click_on_screen(x, y:integer);
var planet_id: integer;
begin
   x := x div zoom;
   y := y div zoom;
   if map[x, y] <> -1 then begin
     planet_id := map[x, y];
     if startplanet = -1 then set_startplanet(planet_id)
     else begin
         if targetplanet = -1 then set_targetplanet(planet_id)
         else begin
             startplanet := -1;
             targetplanet := -1;
             form1.label2.Caption := 'Please select a planet';
         end;
         end;
   end;
   form1.DEBUGLABEL.Caption := inttostr(startplanet)+';'+inttostr(targetplanet);

end;

constructor Tgame.create(nx, ny, new_player_nr, planet_nr:integer);
var tx, ty, i, j: integer;
    player: Tplayer;
    input: string;
begin
  //initialisation of variables
  input := '0';
  InputQuery('width', 'type a number', input);
  x := strtoint(input);
  InputQuery('height', 'type a number', input);
  y := strtoint(input);
  InputQuery('player nr', 'type a number', input);
  new_player_nr := strtoint(input);
  InputQuery('planet nr', 'type a number', input);
  planet_nr := strtoint(input);
  //x := nx;
  //y := ny;
  zoom := 20;
  {form1.image1.width := zoom*x;
  form1.image1.height := zoom*y; }
  form1.image1.width := 750;
  form1.image1.height  := 500;
  turn := 0;
  player_on_turn := 0;
  player_nr := new_player_nr;
  reset_labels();

  randomize();

  //players
  SetLength(players, player_nr);
  for i:=low(players) to high(players) do begin
      player := TPlayer.create(i);
      players[i] := player;
      //showmessage(inttostr(i));
  end;

  //ships
  setlength(ships, 0);

  //map
  SetLength(map, x, y);
  for tx:=low(map) to high(map) do begin
    for ty:=low(map[low(map)]) to high(map[high(map)]) do begin
      map[tx, ty] := -1;
    end;
  end;

  //planets
  j := 0;
  setlength(planets, planet_nr);
  randomize;
  for i:=low(planets) to high(planets) do begin
  repeat
    tx := random(x);
    ty := random(y);
  until map[tx, ty] = -1;
  map[tx, ty] := i;

  if j < player_nr then begin
      planets[i] := Tplanet.create(j, tx, ty, true);
      end
  else planets[i] := Tplanet.create(-1, tx, ty, false);
  j := j+1;
  end;
  refresh_screen();
end;

procedure Tgame.next_player();
var
    i, j, attack_result, testowner: integer;
    landplanet, planet: Tplanet;
    status: boolean;
begin
  reset_labels();

  //set player
  player_on_turn := player_on_turn + 1;
  //showmessage(inttostr(player_on_turn)+';'+inttostr(player_nr));
  if player_on_turn >= player_nr then begin
      player_on_turn := 0;
      turn := turn + 1;
  end;

  //planet turn start
  for i:=low(planets) to high(planets) do begin
      planets[i].turn_start(player_on_turn);
  end;
  i := 0;

  //fly spaceships
  for i := low(ships) to high(ships) do begin
      if ships[i].on_step(player_on_turn) then
      begin
          //ATTACK!!!!
          landplanet := planets[map[ships[i].tx, ships[i].ty]];

          //fight result
          attack_result :=  landplanet.ships - ships[i].get_attack();
          if attack_result < 0 then begin
              //ships won the attack...
              landplanet.ships := -attack_result;
              landplanet.owner := ships[i].owner;
          end else landplanet.ships := attack_result;  //ships lost

          //delete ship
          for j:=i to high(ships) do begin
              if j <> high(ships) then begin
                  ships[j] := ships[j+1];
              end;
          end;
          setlength(ships, length(ships)-1);

          //because next ships is now current:
          if length(ships) <> 0 then begin
              ships[i].on_step(player_on_turn)
          end;
      end;
  end;

  //win?
  testowner := -1;
  status := true;
  for i:=low(planets) to high(planets) do begin
     planet := planets[i];
     if (testowner <> -1) and (planet.owner <> -1) and
        (planet.owner <> testowner) then begin
         status := false;
     end;
     if planet.owner <> -1 then begin
         testowner := planet.owner;
     end;
  end;
  if status then begin
      if testowner <> -1 then showmessage(inttostr(testowner)+' won the game!')
      else showmessage('all players lost!');
  end;

  //finish
  refresh_screen();
end;

procedure Tgame.refresh_screen();
var tx, ty, i, sx, sy: integer;
    planet: Tplanet;
    ship: TSpaceship;
begin
  with form1.image1 do begin
      //clear screen
      canvas.brush.color := clBlack;
      canvas.clear;

  end;


  //draw planets
  for tx:=low(map) to high(map) do begin
    for ty:=low(map[low(map)]) to high(map[high(map)]) do begin
       //showmessage(inttostr(tx)+inttostr(ty));
       with Form1.Image1.Canvas do begin
           if map[tx, ty] <> -1 then begin
           planet:= planets[map[tx, ty]];
           brush.color := planet.color;
           if planet.owner = player_on_turn then begin
               pen.color := clwhite;
               pen.width := 3;
               ellipse(tx*zoom+1, ty*zoom+1, tx*zoom+zoom, ty*zoom+zoom);
               //reset pen
               pen.color := clBlack;
               pen.width := 1;
           end else ellipse(tx*zoom+1, ty*zoom+1, tx*zoom+zoom, ty*zoom+zoom);

           if planet.owner <> -1 then begin
               brush.color := players[planet.owner].color;
               ellipse(tx*zoom+4, ty*zoom+4, tx*zoom+zoom-3, ty*zoom+zoom-3);
           end;
           end;
       end;
    end;
  end;
  //draw spaceships
  for i := low(ships) to high(ships) do begin
      ship := ships[i];
      sx := round(ship.x*zoom);
      sy := round(ship.y*zoom);
      if ship.owner = player_on_turn then begin
        with Form1.Image1.Canvas do begin
          brush.color := clred;
          ellipse(sx+6, sy+6, sx+zoom-5, sy+zoom-5);

        end;

      end;
  end;
  //draw selection cross
  //startplanet first
  if startplanet <> -1 then begin
      planet := planets[startplanet];
      with Form1.Image1.Canvas do begin
          pen.color := clRed;
          pen.width := 3;
          moveto(planet.x*zoom+4, planet.y*zoom+4);
          lineto(planet.x*zoom+zoom-4, planet.y*zoom+zoom-4);
          moveto(planet.x*zoom+zoom-4, planet.y*zoom+4);
          lineto(planet.x*zoom+4, planet.y*zoom+zoom-4);

          //reset pen
          pen.color := clBlack;
          pen.width := 1;
      end;
  end;
  if targetplanet <> -1 then begin
      planet := planets[targetplanet];
      with Form1.Image1.Canvas do begin
          pen.color := clGreen;
          pen.width := 3;
          moveto(planet.x*zoom+4, planet.y*zoom+4);
          lineto(planet.x*zoom+zoom-4, planet.y*zoom+zoom-4);
          moveto(planet.x*zoom+zoom-4, planet.y*zoom+4);
          lineto(planet.x*zoom+4, planet.y*zoom+zoom-4);

          //reset pen
          pen.color := clBlack;
          pen.width := 1;
      end;
  end;

  //set Labels
  //form1.Label2.Caption := 'Please select a planet';
  form1.label1.Caption := 'Turn: '+inttostr(turn)+'  Player: '+
      inttostr(player_on_turn);
end;

procedure Tgame.set_startplanet(planet_id:integer);
var planet: TPlanet;
begin
    planet := planets[planet_id];
    if player_on_turn = planet.owner then begin
        startplanet := planet_id;
        get_planet_info(planet_id, player_on_turn);
        refresh_screen();
        form1.label2.Caption := 'Please select a target planet';
    end;
end;

procedure Tgame.set_targetplanet(planet_id:integer);
begin
    if planet_id <> startplanet then begin
        targetplanet := planet_id;
        get_planet_info(planet_id, player_on_turn);
        refresh_screen();
        form1.label2.Caption := 'Please select a spaceship number and confirm';
    end;
end;

procedure Tgame.reset_labels();
begin
    startplanet := -1;
    targetplanet := -1;
    form1.Infolabel.Caption := '';
    form1.Label2.Caption := 'Please select a planet';
end;

function Tgame.send(nr: integer): boolean;
var
    fx, fy,tx, ty, owner, effective, len: integer;
begin
  if targetplanet <> -1 then begin
      if planets[startplanet].ships >= nr then begin
          //create spaceship
          fx := planets[startplanet].x;
          fy := planets[startplanet].y;
          tx := planets[targetplanet].x;
          ty := planets[targetplanet].y;
          owner := planets[startplanet].owner;
          effective := planets[startplanet].kill_percent;
          setlength(ships, length(ships)+1);
          ships[high(ships)] := TSpaceship.create(fx, fy, tx, ty, owner, nr, effective);

          //remove nr from planet
          planets[startplanet].ships := planets[startplanet].ships - nr;

          //reset
          reset_labels();
          refresh_screen();
      end else begin
          reset_labels();
          form1.infolabel.Caption := 'not enought ships on planet!!!';
          refresh_screen();
      end;
  end;
end;

function Tgame.get_planet_info(planet_id, player: integer): string;
var planet: TPlanet;
begin
planet := planets[planet_id];
if player_on_turn = planet.owner then begin
form1.infolabel.caption := 'Owner: '+inttostr(planet.owner)
    +sLineBreak+'Ships: '+inttostr(planet.ships)
    +sLineBreak+'Production: '+inttostr(planet.production)
    +sLineBreak+'Kill Percentage: '+inttostr(planet.kill_percent);
end else begin
form1.infolabel.caption := 'Owner: '+inttostr(planet.owner);
end;
end;

end.

