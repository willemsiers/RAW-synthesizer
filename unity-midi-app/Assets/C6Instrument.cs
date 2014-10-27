using UnityEngine;
using System.Collections;

public class C6Instrument : MonoBehaviour, IInstrument {
	public string iName;
	private AudioSource[] CArr = new AudioSource[6];

	void Start () {
		CArr[0] = (AudioSource) transform.Find("c2").GetComponent("AudioSource");
		CArr[1] = (AudioSource) transform.Find("c3").GetComponent("AudioSource");
		CArr[2] = (AudioSource) transform.Find("c4").GetComponent("AudioSource");
		CArr[3] = (AudioSource) transform.Find("c5").GetComponent("AudioSource");
		CArr[4] = (AudioSource) transform.Find("c6").GetComponent("AudioSource");
		CArr[5] = (AudioSource) transform.Find("c7").GetComponent("AudioSource");

		Midi.register (this);
		//StartCoroutine(test ());
	}

	public string getName () {
		return iName;
	}

	private IEnumerator test () {
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 12; j++) {
				playNote(new Vector2(i+3,j));
				yield return new WaitForSeconds(0.5f);
			}
		}
		//yield return new WaitForSeconds(1);
		//playNote (ConvNote.convert (("d3")));
	}

	public bool playNote (Vector2 pitch) {
		//print (pitch);
		// F# - C - F  // F# = 6 // F = 5 // C = 0
		if (pitch.x >= 2 && pitch.x <= 7) {
			CArr[(int)pitch.x - 2].pitch = Mathf.Pow(2, (pitch.y)/12.0f);
			CArr[(int)pitch.x - 2].Play();
		} else {
			return false;
		}
		//instrument.pitch =  Mathf.Pow(2, (note.x + note.y)/12.0f);
		return true;
	}
}
