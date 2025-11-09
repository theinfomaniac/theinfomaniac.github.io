// script.js — p5.js version of Snack Dash
let SCREEN_W = 240;
let SCREEN_H = 160;
let scaleFactor = 3;

let catcher;
let items = [];
let maxItems = 6;
let fps = 60;
let gameSeconds = 20;
let gameFrames = fps * gameSeconds;
let frames = 0;
let spawnTimer = 0;
let spawnInterval = 15;
let score = 0;
let running = true;

function setup(){
  let cnv = createCanvas(SCREEN_W * scaleFactor, SCREEN_H * scaleFactor);
  cnv.parent('game');
  frameRate(fps);
  pixelDensity(1);
  catcher = { x: SCREEN_W/2 - 10, y: SCREEN_H - 18, w:20, h:8 };
  resetItems();
}

function resetItems(){
  items = [];
  for(let i=0;i<maxItems;i++) items.push({alive:false, x:0, y:0, vy:1});
}

function draw(){
  scale(scaleFactor);
  // background
  background(12,20,12);

  if(running){
    frames++;
    // input
    if(keyIsDown(LEFT_ARROW) || keyIsDown(65)) catcher.x -= 3;
    if(keyIsDown(RIGHT_ARROW) || keyIsDown(68)) catcher.x += 3;
    catcher.x = constrain(catcher.x, 0, SCREEN_W - catcher.w);

    spawnTimer++;
    if(spawnTimer >= spawnInterval){
      spawnTimer = 0;
      for(let i=0;i<items.length;i++){
        if(!items[i].alive){
          items[i].alive = true;
          items[i].x = floor(random(3, SCREEN_W - 6));
          items[i].y = -6;
          items[i].vy = 1 + floor(frames / (fps*5));
          break;
        }
      }
    }
    if(frames % (fps*4) === 0 && spawnInterval > 6) spawnInterval--;

    for(let it of items){
      if(it.alive){
        it.y += it.vy;
        if(it.y >= catcher.y - 2){
          if(it.x >= catcher.x - 2 && it.x <= catcher.x + catcher.w + 2){
            it.alive = false;
            score++;
          } else if(it.y > SCREEN_H){
            it.alive = false;
          }
        }
      }
    }

    if(frames >= gameFrames){
      running = false;
    }
  } else {
    // wait for 'A' key (Z) to restart
  }

  // draw items
  noStroke();
  fill(255,255,0);
  for(let it of items){
    if(it.alive){
      rect(it.x-2, it.y-2, 5, 5);
      fill(255);
      rect(it.x-1, it.y-1, 1, 1);
      fill(255,255,0);
    }
  }

  // catcher
  fill(255,0,0);
  rect(catcher.x, catcher.y, catcher.w, catcher.h);
  fill(255);
  rect(catcher.x+3, catcher.y-6, 1, 1);
  rect(catcher.x+catcher.w-4, catcher.y-6, 1, 1);

  // HUD
  fill(255);
  textSize(6);
  textAlign(LEFT, TOP);
  let framesLeft = running ? (gameFrames - frames) : 0;
  let secondsLeft = Math.ceil(framesLeft / fps);
  text("TIME: " + secondsLeft, 4, 4);
  text("SCORE: " + score, 4, 14);

  if(!running){
    push();
    fill(0, 0, 0, 160);
    rect(20,50,200,60);
    fill(255, 255, 0);
    textSize(12);
    textAlign(CENTER, CENTER);
    text("TIME'S UP! SCORE: " + score, 120, 80);
    textSize(8);
    text("Press Z (or Click) to restart", 120, 100);
    pop();
  }
}

function keyPressed(){
  if(!running && (keyCode === 90 || keyCode === 32)){ // Z or Space
    restart();
  }
}

function mousePressed(){
  // allow clicking to restart in web build
  if(!running) restart();
}

function restart(){
  frames = 0;
  spawnTimer = 0;
  spawnInterval = 15;
  score = 0;
  running = true;
  resetItems();
}
