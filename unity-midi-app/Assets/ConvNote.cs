using UnityEngine;
using System.Collections;

public class ConvNote {
	public static Vector2 convert (string note) {
		Vector2 result = new Vector2 (0, 0);
		note = note.ToUpper ();
		string noteStr;
		if (note.Length == 2) {
			noteStr = note.Substring (0, 1);
		}
		else if (note.Length == 3) {
			noteStr = note.Substring (0, 1) + note.Substring (2, 1);
		} else {
			return  Vector2.zero;
		}
		result.x = int.Parse(note.Substring(1,1));
		switch(noteStr) {
			case "C":
				result.y = 0;
				break;
			case "C#":
				result.y = 1;
				break;
			case "D":
				result.y = 2;
				break;
			case "D#":
				result.y = 3;
				break;
			case "E":
				result.y = 4;
				break;
			case "F":
				result.y = 5;
				break;
			case "F#":
				result.y = 6;
				break;
			case "G":
				result.y = 7;
				break;
			case "G#":
				result.y = 8;
				break;
			case "A":
				result.y = 9;
				break;
			case "A#":
				result.y = 10;
				break;
			case "B":
				result.y = 11;
				break;
			default:
				result.y = 0;
				break;
		}
		return result;
	}
}
