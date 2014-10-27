using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Midi : MonoBehaviour {

	AudioSource error;
	private static Dictionary<string,IInstrument> instruments = new Dictionary<string,IInstrument>();

	void Start () {
		error = (AudioSource) transform.GetComponent("AudioSource");
	}

	public void playNote (string note) {
		if(note.Contains(":")) { 
			string[] noteArr = note.Split(':');
			if(noteArr.Length==2) {
				playNote(ConvNote.convert (noteArr[0]),noteArr[1]);
			} else {
				playError();
			}
		} else {
			playNote (ConvNote.convert (note),"piano");
		}
	}

	public void playNote (Vector2 note, string instr) {
		if (!instruments.ContainsKey(instr) || !instruments [instr].playNote (note)) {
			playError();
		}
	}

	public void playError () {
		error.Play ();
	}

	public static void register (IInstrument instr) {
		Midi.instruments.Add (instr.getName(), instr);
	}
}
