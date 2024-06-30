/**
Copyright (c) 2024 Yuya KITANO
Released under the MIT license
https://opensource.org/licenses/mit-license.php
*/

'use strict';

const express = require("express");
const router = express.Router();
const path = require("path");
const fs = require('fs');
const subproc = require('child_process');
const multer  = require('multer');

const multerStorage = multer.diskStorage({
	destination (req, file, cb) {
		cb(null, './app/gmsh/');
	},
	filename (req, file, cb) {
		// https://github.com/expressjs/multer/issues/1104#issuecomment-1155334173
		file.originalname = Buffer.from(file.originalname, 'latin1').toString('utf8');
		cb(null, file.originalname);
	}
});

const upload = multer({
	storage: multerStorage
});

//==================================================================
function exec_png2stl(fname)
{
	// ------------------------------------------------------
	// .png -> .stl
	//
	// https://t-salad.com/node-exe/
	subproc.execSync('py  ./app/gmsh/png2stl.py  "./' + fname + '"');
	// ------------------------------------------------------
}
//==================================================================
function clearPngMshStl_init(dir)
{
	const arrDirFiles = fs.readdirSync(dir, { withFileTypes: true });
	const arrFiles = arrDirFiles.filter(dirent => dirent.isFile()).map(({ name }) => name);
	
	arrFiles.forEach(fname => {
		if (path.basename(fname) == 'blockSpinner.png' || path.basename(fname) == 'png2stl_Cntr.png' || path.basename(fname) == 'png2stl_Mesh.png' || path.parse(fname).ext == ".msh" || path.parse(fname).ext == ".stl") {
			fs.unlink((dir + fname), (error) => {
				if (error != null) {
					console.log(error);
				} else {
					console.log((dir + fname) + " : deleted");
				}
			});
		}
	});
}
//==================================================================
function clearPngMshStl_all(dir)
{
	const arrDirFiles = fs.readdirSync(dir, { withFileTypes: true });
	const arrFiles = arrDirFiles.filter(dirent => dirent.isFile()).map(({ name }) => name);
	
	arrFiles.forEach(fname => {
		if (path.parse(fname).ext == ".png" || path.parse(fname).ext == ".msh" || path.parse(fname).ext == ".stl") {
			fs.unlink((dir + fname), (error) => {
				if (error != null) {
					console.log(error);
				} else {
					console.log((dir + fname) + " : deleted");
				}
			});
		}
	});
}
//==================================================================
// https://zenn.dev/wkb/books/node-tutorial/viewer/todo_03

// --------------------------------------
router.get("/", (req, res) => {
	clearPngMshStl_all("./app/gmsh/");
	fs.copyFileSync("blockSpinner.png","./app/gmsh/blockSpinner.png")
	fs.copyFileSync("png2stl_Cntr.png","./app/gmsh/png2stl_Cntr.png")
	fs.copyFileSync("png2stl_Mesh.png","./app/gmsh/png2stl_Mesh.png")
	res.render("./index.ejs");
});
// --------------------------------------
router.post("/", upload.any(), (req, res) => {
	clearPngMshStl_init("./app/gmsh/");
	
	// sout
	console.log('# originalname : ' + req.files[0].originalname);
	// console.log('# destination : ' + req.files[0].destination);
	let fname_stl = req.files[0].originalname.split('.').slice(0, -1).join('.') + '.stl';
	console.log();
	console.log('loaded : ');
	console.log(req.files[0]);
	console.log();
	
	// ## OPERATION ##
	exec_png2stl(req.files[0].originalname);
	
	// sout
	console.log('# RETURN : ' + fname_stl);
	console.log();
	
	// https://qiita.com/watatakahashi/items/4b456971ae6dc3038569#%E6%96%B9%E6%B3%95%E3%81%9D%E3%81%AE2-header%E3%81%AB%E6%8C%87%E5%AE%9A
	res.set({
		'Content-Disposition': `attachment; filename=${encodeURIComponent(fname_stl)}`
	});
	
	fs.copyFileSync("blockSpinner.png","./app/gmsh/blockSpinner.png")
	
	res.status(200).send(
		fs.readFileSync(req.files[0].destination + fname_stl)
	);
	
	// res.redirect('/');
});
// --------------------------------
module.exports = router;
